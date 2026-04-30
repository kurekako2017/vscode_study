package com.jtspringproject.JtSpringProject.batch.quartz;

import com.jtspringproject.JtSpringProject.batch.service.ProductInventoryCheckBatchService;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.quartz.QuartzJobBean;

/**
 * 商品在庫整合チェックを Quartz から呼び出すジョブ。
 */
public class ProductInventoryCheckQuartzJob extends QuartzJobBean {

    private static final Logger logger =
        LoggerFactory.getLogger(ProductInventoryCheckQuartzJob.class);

    @Autowired
    private ProductInventoryCheckBatchService batchService;

    @Override
    protected void executeInternal(JobExecutionContext context) throws JobExecutionException {
        try {
            int exitCode = batchService.runBatch();
            logger.info("Quartz 商品在庫整合チェックジョブを実行しました。exitCode={}", exitCode);
        } catch (Exception exception) {
            throw new JobExecutionException("Quartz 商品在庫整合チェックジョブの実行に失敗しました。", exception);
        }
    }
}
