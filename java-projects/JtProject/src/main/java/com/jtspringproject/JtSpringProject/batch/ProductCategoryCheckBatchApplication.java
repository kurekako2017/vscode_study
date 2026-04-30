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
 * 商品·分類マスタ整合チェック用バッチ起動クラス（BAT-005）。
 *
 * <p>Spring Boot を非 Web モードで起動し、
 * バッチ処理用の専用コンテキストを構築する。</p>
 *
 * <h3>実行方法：</h3>
 * <pre>
 * java -cp "..." \
 *   com.jtspringproject.JtSpringProject.batch.launcher.ProductCategoryCheckBatchApplication
 * </pre>
 *
 * または：
 *
 * <pre>
 * mvn exec:java -Dexec.mainClass="..." \
 *   -Dspring.profiles.active=batch
 * </pre>
 *
 * @author JT Spring Project Team
 * @version 1.0
 */
public final class ProductCategoryCheckBatchApplication {

    private static final Logger logger = LoggerFactory.getLogger(ProductCategoryCheckBatchApplication.class);

    private ProductCategoryCheckBatchApplication() {
    }

    /**
     * バッチの起動入口。
     *
     * <p>以下の処理を行う：
     * 1. Spring Boot を batch プロファイルで非 Web 起動
     * 2. ProductCategoryCheckBatchService をインジェクション
     * 3. runBatch() メソッドを実行
     * 4. 終了コードを返却
     * </p>
     *
     * @param args コマンドライン引数（現在は使用しない）
     */
    public static void main(String[] args) {
        logger.info("商品·分類マスタ整合チェックバッチ（BAT-005）を起動します。");

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
            logger.error("商品·分類マスタ整合チェックバッチの実行に失敗しました。", exception);
        } finally {
            final int finalExitCode = exitCode;
            int springExitCode = SpringApplication.exit(context, () -> finalExitCode);
            System.exit(springExitCode);
        }
    }
}
