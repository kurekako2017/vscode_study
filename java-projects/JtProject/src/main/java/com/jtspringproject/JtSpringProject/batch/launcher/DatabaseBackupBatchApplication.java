package com.jtspringproject.JtSpringProject.batch.launcher;

import com.jtspringproject.JtSpringProject.JtSpringProjectApplication;
import com.jtspringproject.JtSpringProject.batch.service.DatabaseBackupBatchService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * BAT-007 DBバックアップバッチ起動クラス。
 *
 * <p>用途: H2 の DB ファイルをタイムスタンプ付きでバックアップディレクトリへコピーする
 * バッチの起動エントリ。運用環境では DB 種別に合わせて専用のバックアップ方式を採用すること。
 *
 * <p>実行手順:
 * <ol>
 *   <li>`JtSpringProjectApplication` を batch プロファイルで非 Web 起動</li>
 *   <li>`DatabaseBackupBatchService` を取得して `runBatch()` を実行</li>
 *   <li>終了コードで Spring を終了し、`System.exit()` を呼び出す</li>
 * </ol>
 *
 * <p>関連設計書: doc/jp-docs/03_database/90_DBバックアップ詳細設計書.md
 */
public final class DatabaseBackupBatchApplication {

    private static final Logger logger = LoggerFactory.getLogger(DatabaseBackupBatchApplication.class);

    private DatabaseBackupBatchApplication() {
    }

    /**
     * バッチの起動入口。
     *
     * @param args コマンドライン引数
     */
    public static void main(String[] args) {
        ConfigurableApplicationContext context =
            new SpringApplicationBuilder(JtSpringProjectApplication.class)
                .profiles("batch")
                .web(WebApplicationType.NONE)
                .logStartupInfo(false)
                .run(args);

        int exitCode = 1;
        try {
            DatabaseBackupBatchService batchService = context.getBean(DatabaseBackupBatchService.class);
            exitCode = batchService.runBatch();
        } catch (Exception exception) {
            logger.error("BAT-007 DBバックアップの実行に失敗しました。", exception);
        } finally {
            final int finalExitCode = exitCode;
            int springExitCode = SpringApplication.exit(context, () -> finalExitCode);
            System.exit(springExitCode);
        }
    }
}