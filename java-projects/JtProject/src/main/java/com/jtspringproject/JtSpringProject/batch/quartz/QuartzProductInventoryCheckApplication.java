package com.jtspringproject.JtSpringProject.batch.quartz;

import com.jtspringproject.JtSpringProject.JtSpringProjectApplication;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.builder.SpringApplicationBuilder;

/**
 * Quartz 学習用の定期実行起動クラス。
 */
public final class QuartzProductInventoryCheckApplication {

    private static final Logger logger =
        LoggerFactory.getLogger(QuartzProductInventoryCheckApplication.class);

    private QuartzProductInventoryCheckApplication() {
    }

    /**
     * Quartz 学習用ランチャー。
     *
     * @param args コマンドライン引数
     */
    public static void main(String[] args) {
        new SpringApplicationBuilder(JtSpringProjectApplication.class)
            .profiles("batch", "quartz-lab")
            .web(WebApplicationType.NONE)
            .logStartupInfo(false)
            .run(args);

        logger.info("Quartz 学習用スケジューラを起動しました。Ctrl+C で停止してください。");
    }
}
