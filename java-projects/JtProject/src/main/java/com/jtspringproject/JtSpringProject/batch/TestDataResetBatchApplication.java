package com.jtspringproject.JtSpringProject.batch.launcher;

import com.jtspringproject.JtSpringProject.JtSpringProjectApplication;
import com.jtspringproject.JtSpringProject.batch.service.TestDataResetBatchService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * BAT-003 テストデータリセットバッチ起動クラス。
 */
/**
 * BAT-003 テストデータリセットバッチ起動クラス。
 *
 * <p>用途: 開発・テスト用に DB を初期状態へ戻すためのバッチ起動エントリ。テスト実行前に
 * 手動で起動して DB を初期化することを想定している。
 *
 * <p>関連設計書: doc/jp-docs/03_database/87_テストデータリセット詳細設計書.md
 */
public final class TestDataResetBatchApplication {

    private static final Logger logger = LoggerFactory.getLogger(TestDataResetBatchApplication.class);

    private TestDataResetBatchApplication() {
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
            TestDataResetBatchService batchService = context.getBean(TestDataResetBatchService.class);
            exitCode = batchService.runBatch();
        } catch (Exception exception) {
            logger.error("BAT-003 テストデータリセットの実行に失敗しました。", exception);
        } finally {
            final int finalExitCode = exitCode;
            int springExitCode = SpringApplication.exit(context, () -> finalExitCode);
            System.exit(springExitCode);
        }
    }
}
