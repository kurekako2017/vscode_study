package com.jtspringproject.JtSpringProject.batch.launcher;

import com.jtspringproject.JtSpringProject.JtSpringProjectApplication;
import com.jtspringproject.JtSpringProject.batch.service.ProductCategoryCheckBatchService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * BAT-005 商品・分類マスタ整合チェックバッチ起動クラス。
 *
 * <p>用途: 商品マスタと分類マスタの整合性をチェックし、CSV に結果を出力するバッチの起動エントリ。
 *
 * <p>関連設計書: doc/jp-docs/03_database/83_模擬バッチ設計書.md
 */
public final class ProductCategoryCheckBatchApplication {

    private static final Logger logger = LoggerFactory.getLogger(ProductCategoryCheckBatchApplication.class);

    private ProductCategoryCheckBatchApplication() {
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
            ProductCategoryCheckBatchService batchService =
                context.getBean(ProductCategoryCheckBatchService.class);
            exitCode = batchService.runBatch();
        } catch (Exception exception) {
            logger.error("商品・分類マスタ整合チェックバッチの実行に失敗しました。", exception);
        } finally {
            final int finalExitCode = exitCode;
            int springExitCode = SpringApplication.exit(context, () -> finalExitCode);
            System.exit(springExitCode);
        }
    }
}