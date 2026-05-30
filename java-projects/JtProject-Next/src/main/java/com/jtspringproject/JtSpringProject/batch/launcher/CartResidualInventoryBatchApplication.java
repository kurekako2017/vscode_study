package com.jtspringproject.JtSpringProject.batch.launcher;

import com.jtspringproject.JtSpringProject.JtSpringProjectApplication;
import com.jtspringproject.JtSpringProject.batch.service.CartResidualInventoryBatchService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * BAT-006 カート残留データ棚卸バッチ起動クラス。
 *
 * <p>用途: `CART` / `CART_PRODUCT` の残留・孤立データを検出するバッチの起動エントリ。
 * 実行により CSV を出力し、必要に応じて削除モードで不要データを削除する。
 *
 * <p>関連設計書: doc/jp-docs/03_database/89_カート残留データ棚卸詳細設計書.md
 */
public final class CartResidualInventoryBatchApplication {

    private static final Logger logger = LoggerFactory.getLogger(CartResidualInventoryBatchApplication.class);

    private CartResidualInventoryBatchApplication() {
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
            CartResidualInventoryBatchService batchService =
                context.getBean(CartResidualInventoryBatchService.class);
            exitCode = batchService.runBatch();
        } catch (Exception exception) {
            logger.error("BAT-006 カート残留データ棚卸の実行に失敗しました。", exception);
        } finally {
            final int finalExitCode = exitCode;
            int springExitCode = SpringApplication.exit(context, () -> finalExitCode);
            System.exit(springExitCode);
        }
    }
}