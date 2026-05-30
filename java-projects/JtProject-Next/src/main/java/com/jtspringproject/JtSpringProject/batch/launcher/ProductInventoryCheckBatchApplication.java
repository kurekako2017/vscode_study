package com.jtspringproject.JtSpringProject.batch.launcher;

import com.jtspringproject.JtSpringProject.JtSpringProjectApplication;
import com.jtspringproject.JtSpringProject.batch.service.ProductInventoryCheckBatchService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * 商品在庫整合チェック用の模擬バッチ起動クラス（BAT-LAB-001）。
 *
 * <p>Spring Boot を非 Web モードで起動し、
 * バッチ処理用の専用コンテキストを構築する。</p>
 *
 * <h3>実行方法：</h3>
 * <pre>
 * java -cp "..." \
 *   com.jtspringproject.JtSpringProject.batch.launcher.ProductInventoryCheckBatchApplication
 * </pre>
 *
 * @author JT Spring Project Team
 * @version 1.0
 */
public final class ProductInventoryCheckBatchApplication {

    private static final Logger logger = LoggerFactory.getLogger(ProductInventoryCheckBatchApplication.class);

    private ProductInventoryCheckBatchApplication() {
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
            ProductInventoryCheckBatchService batchService =
                context.getBean(ProductInventoryCheckBatchService.class);
            exitCode = batchService.runBatch();
        } catch (Exception exception) {
            logger.error("商品在庫整合チェックバッチの実行に失敗しました。", exception);
        } finally {
            final int finalExitCode = exitCode;
            int springExitCode = SpringApplication.exit(context, () -> finalExitCode);
            System.exit(springExitCode);
        }
    }
}