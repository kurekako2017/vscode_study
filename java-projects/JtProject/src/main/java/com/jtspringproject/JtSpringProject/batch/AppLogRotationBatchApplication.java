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
