package com.jtspringproject.JtSpringProject.batch;

import java.util.LinkedHashMap;
import java.util.Map;
import javax.sql.DataSource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Profile;
import org.springframework.core.io.ClassPathResource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.init.DatabasePopulatorUtils;
import org.springframework.jdbc.datasource.init.ResourceDatabasePopulator;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * BAT-003 テストデータリセットバッチ本体。
 */
@Service
@Profile("batch")
public class TestDataResetBatchService {

    private static final Logger logger = LoggerFactory.getLogger(TestDataResetBatchService.class);

    private final JdbcTemplate jdbcTemplate;
    private final DataSource dataSource;

    public TestDataResetBatchService(JdbcTemplate jdbcTemplate, DataSource dataSource) {
        this.jdbcTemplate = jdbcTemplate;
        this.dataSource = dataSource;
    }

    /**
     * バッチを実行する。
     *
     * @return 終了コード
     */
    @Transactional
    public int runBatch() {
        logger.info("BAT-003 テストデータリセットを開始します。");
        try {
            Map<String, Integer> deleted = cleanupTables();
            initializeData();
            logger.info("BAT-003 が完了しました。削除件数: {}", deleted);
            return 0;
        } catch (Exception exception) {
            logger.error("BAT-003 の実行中にエラーが発生しました。", exception);
            return 1;
        }
    }

    private Map<String, Integer> cleanupTables() {
        Map<String, Integer> deleted = new LinkedHashMap<>();
        deleted.put("CART_PRODUCT", jdbcTemplate.update("DELETE FROM CART_PRODUCT"));
        deleted.put("CART", jdbcTemplate.update("DELETE FROM CART"));
        deleted.put("PRODUCT", jdbcTemplate.update("DELETE FROM PRODUCT"));
        deleted.put("CATEGORY", jdbcTemplate.update("DELETE FROM CATEGORY"));
        deleted.put("CUSTOMER", jdbcTemplate.update("DELETE FROM CUSTOMER"));
        return deleted;
    }

    private void initializeData() {
        ResourceDatabasePopulator populator =
            new ResourceDatabasePopulator(new ClassPathResource("data.sql"));
        populator.setContinueOnError(true);
        populator.setSeparator(";");
        DatabasePopulatorUtils.execute(populator, dataSource);
    }
}
