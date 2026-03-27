package com.jtspringproject.JtSpringProject.batch;

import com.jtspringproject.JtSpringProject.JtSpringProjectApplication;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * 商品在庫整合チェック用の模擬バッチ起動クラス。
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
