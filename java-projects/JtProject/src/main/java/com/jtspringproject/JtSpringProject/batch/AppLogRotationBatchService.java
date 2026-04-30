package com.jtspringproject.JtSpringProject.batch;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Service;

/**
 * BAT-004 アプリケーションログローテーションバッチ本体。
 *
 * <p>概要: 指定ディレクトリ内のログファイル（拡張子 `.log`）を検索し、
 * 各ファイルを ZIP 圧縮して保存した後、元のログファイルを切り詰め（truncate）する処理を行う。
 * 通常の運用ではログローテーションやバックアップ目的で定期実行する。
 *
 * <p>注意点:
 * - 圧縮中にファイルが書き込み中の場合は I/O エラーになる可能性があるため、
 *   実運用ではアプリケーションのログ設定や排他制御を検討すること。
 * - デフォルトの対象ディレクトリは `logs/batch`（`batch.log.rotation.dir` で上書き可）。
 *
 * <p>関連設計書: doc/jp-docs/03_database/88_アプリケーションログローテーション詳細設計書.md
 */
@Service
@Profile("batch")
public class AppLogRotationBatchService {

    private static final Logger logger = LoggerFactory.getLogger(AppLogRotationBatchService.class);
    private static final DateTimeFormatter TS = DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss");

    @Value("${batch.log.rotation.dir:logs/batch}")
    private String logDir;

    /**
     * バッチを実行する。
     *
     * <p>主な処理:
     * <ol>
     *   <li>指定ディレクトリから `.log` ファイルを収集する（サイズが 0 より大きいファイルのみ）</li>
     *   <li>各ログファイルを ZIP に圧縮して同一ディレクトリに保存</li>
     *   <li>元のログファイルを切り詰め（中身を消す）して空にする</li>
     * </ol>
     *
     * @return 終了コード: 0=正常終了、1=システムエラー、2=（将来の用途用）業務NG
     */
    public int runBatch() {
        logger.info("BAT-004 ログローテーションを開始します。対象ディレクトリ: {}", logDir);
        try {
            Path dir = Paths.get(logDir);
            if (!Files.exists(dir)) {
                logger.warn("ログディレクトリが存在しません。ローテーション対象なし: {}", dir.toAbsolutePath());
                return 0;
            }

            List<Path> targets = findLogFiles(dir);
            int rotated = 0;
            for (Path logFile : targets) {
                rotateSingleFile(logFile);
                rotated++;
            }
            logger.info("BAT-004 が完了しました。ローテーション件数: {}", rotated);
            return 0;
        } catch (Exception exception) {
            logger.error("BAT-004 の実行中にエラーが発生しました。", exception);
            return 1;
        }
    }

    private List<Path> findLogFiles(Path dir) throws IOException {
        List<Path> files = new ArrayList<>();
        try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir, "*.log")) {
            for (Path path : stream) {
                if (Files.isRegularFile(path) && Files.size(path) > 0L) {
                    files.add(path);
                }
            }
        }
        return files;
    }

    private void rotateSingleFile(Path logFile) throws IOException {
        String timestamp = TS.format(LocalDateTime.now());
        String zipName = logFile.getFileName().toString() + "." + timestamp + ".zip";
        Path zipPath = logFile.getParent().resolve(zipName);

        try (OutputStream fos = Files.newOutputStream(zipPath, StandardOpenOption.CREATE_NEW);
             ZipOutputStream zos = new ZipOutputStream(fos);
             InputStream in = Files.newInputStream(logFile)) {
            ZipEntry entry = new ZipEntry(logFile.getFileName().toString());
            zos.putNextEntry(entry);
            in.transferTo(zos);
            zos.closeEntry();
        }

        Files.newBufferedWriter(logFile, StandardOpenOption.TRUNCATE_EXISTING).close();
        logger.info("ローテーション完了: {} -> {}", logFile.toAbsolutePath(), zipPath.toAbsolutePath());
    }
}
