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
     * @return 終了コード
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
