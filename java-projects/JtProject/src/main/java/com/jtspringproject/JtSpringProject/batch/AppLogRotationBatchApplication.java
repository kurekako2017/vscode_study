package com.jtspringproject.JtSpringProject.batch;

import com.jtspringproject.JtSpringProject.JtSpringProjectApplication;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * BAT-004 アプリケーションログローテーションバッチ起動クラス。
 *
 * <p>用途: アプリケーションのログファイルをローテーション（ZIP 圧縮して元ファイルを切り詰める）するバッチの起動エントリ。
 * このクラスは Spring Boot を非 Web モードで起動し、`AppLogRotationBatchService` の `runBatch()` を実行して終了コードを返却する。
 *
 * <p>実行手順:
 * <ol>
 *   <li>`JtSpringProjectApplication` を Spring Application として起動（プロファイル: `batch`）</li>
 *   <li>`AppLogRotationBatchService` を取得して `runBatch()` を実行</li>
 *   <li>実行結果の終了コードで Spring を終了し、`System.exit()` を呼び出す</li>
 * </ol>
 *
 * <p>関連設計書: doc/jp-docs/03_database/88_アプリケーションログローテーション詳細設計書.md
 */
public final class AppLogRotationBatchApplication {

    private static final Logger logger = LoggerFactory.getLogger(AppLogRotationBatchApplication.class);

    private AppLogRotationBatchApplication() {
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
            AppLogRotationBatchService batchService = context.getBean(AppLogRotationBatchService.class);
            exitCode = batchService.runBatch();
        } catch (Exception exception) {
            logger.error("BAT-004 ログローテーションの実行に失敗しました。", exception);
        } finally {
            final int finalExitCode = exitCode;
            int springExitCode = SpringApplication.exit(context, () -> finalExitCode);
            System.exit(springExitCode);
        }
    }
}
