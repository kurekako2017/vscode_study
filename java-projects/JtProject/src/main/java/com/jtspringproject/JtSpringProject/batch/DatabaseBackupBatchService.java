package com.jtspringproject.JtSpringProject.batch;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Service;

/**
 * BAT-007 DBバックアップバッチ本体。
 */
@Service
@Profile("batch")
public class DatabaseBackupBatchService {

    private static final Logger logger = LoggerFactory.getLogger(DatabaseBackupBatchService.class);
    private static final DateTimeFormatter TS = DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss");

    @Value("${batch.db.file:batch-work/jtproject-batch.mv.db}")
    private String sourceDbFile;

    @Value("${batch.db.trace-file:batch-work/jtproject-batch.trace.db}")
    private String sourceTraceFile;

    @Value("${batch.db.backup.dir:batch-backup}")
    private String backupDir;

    /**
     * バッチを実行する。
     *
     * @return 終了コード
     */
    public int runBatch() {
        logger.info("BAT-007 DBバックアップを開始します。source={}", sourceDbFile);
        try {
            Path source = Paths.get(sourceDbFile);
            if (!Files.exists(source)) {
                logger.warn("バックアップ対象 DB ファイルが存在しません: {}", source.toAbsolutePath());
                return 2;
            }

            Path backupDirPath = Paths.get(backupDir);
            Files.createDirectories(backupDirPath);

            String ts = TS.format(LocalDateTime.now());
            Path target = backupDirPath.resolve("jtproject-batch-" + ts + ".mv.db");
            Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);

            Path trace = Paths.get(sourceTraceFile);
            if (Files.exists(trace)) {
                Path traceTarget = backupDirPath.resolve("jtproject-batch-" + ts + ".trace.db");
                Files.copy(trace, traceTarget, StandardCopyOption.REPLACE_EXISTING);
            }

            logger.info("BAT-007 が完了しました。バックアップファイル: {}", target.toAbsolutePath());
            return 0;
        } catch (IOException exception) {
            logger.error("BAT-007 の実行中にエラーが発生しました。", exception);
            return 1;
        }
    }
}
