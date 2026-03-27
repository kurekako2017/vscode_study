package com.jtspringproject.JtSpringProject.batch.quartz;

import java.util.Properties;
import org.quartz.JobDetail;
import org.quartz.SimpleTrigger;
import org.quartz.Trigger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.scheduling.quartz.JobDetailFactoryBean;
import org.springframework.scheduling.quartz.SchedulerFactoryBean;
import org.springframework.scheduling.quartz.SimpleTriggerFactoryBean;

/**
 * Quartz 学習用バッチ設定。
 */
@Configuration
@Profile("quartz-lab")
public class QuartzBatchLabConfig {

    @Value("${lab.quartz.productInventoryCheck.intervalMs:60000}")
    private long intervalMs;

    @Value("${lab.quartz.productInventoryCheck.startDelayMs:5000}")
    private long startDelayMs;

    @Bean
    public AutowiringSpringBeanJobFactory quartzJobFactory(ApplicationContext applicationContext) {
        AutowiringSpringBeanJobFactory jobFactory = new AutowiringSpringBeanJobFactory();
        jobFactory.setApplicationContext(applicationContext);
        return jobFactory;
    }

    @Bean
    public JobDetailFactoryBean productInventoryCheckJobDetail() {
        JobDetailFactoryBean factoryBean = new JobDetailFactoryBean();
        factoryBean.setJobClass(ProductInventoryCheckQuartzJob.class);
        factoryBean.setName("productInventoryCheckQuartzJob");
        factoryBean.setDescription("商品在庫整合チェックの Quartz 学習用ジョブ");
        factoryBean.setDurability(true);
        return factoryBean;
    }

    @Bean
    public SimpleTriggerFactoryBean productInventoryCheckTrigger(JobDetail productInventoryCheckJobDetail) {
        SimpleTriggerFactoryBean factoryBean = new SimpleTriggerFactoryBean();
        factoryBean.setJobDetail(productInventoryCheckJobDetail);
        factoryBean.setName("productInventoryCheckQuartzTrigger");
        factoryBean.setStartDelay(startDelayMs);
        factoryBean.setRepeatInterval(intervalMs);
        factoryBean.setRepeatCount(SimpleTrigger.REPEAT_INDEFINITELY);
        factoryBean.setMisfireInstruction(SimpleTrigger.MISFIRE_INSTRUCTION_RESCHEDULE_NEXT_WITH_REMAINING_COUNT);
        return factoryBean;
    }

    @Bean
    public SchedulerFactoryBean schedulerFactoryBean(
        AutowiringSpringBeanJobFactory quartzJobFactory,
        Trigger productInventoryCheckTrigger,
        JobDetail productInventoryCheckJobDetail) {

        SchedulerFactoryBean factoryBean = new SchedulerFactoryBean();
        factoryBean.setJobFactory(quartzJobFactory);
        factoryBean.setJobDetails(productInventoryCheckJobDetail);
        factoryBean.setTriggers(productInventoryCheckTrigger);
        factoryBean.setOverwriteExistingJobs(true);
        factoryBean.setAutoStartup(true);
        factoryBean.setWaitForJobsToCompleteOnShutdown(true);
        factoryBean.setQuartzProperties(quartzProperties());
        return factoryBean;
    }

    private Properties quartzProperties() {
        Properties properties = new Properties();
        properties.setProperty("org.quartz.scheduler.instanceName", "jtprojectQuartzLabScheduler");
        properties.setProperty("org.quartz.threadPool.threadCount", "2");
        properties.setProperty("org.quartz.jobStore.class", "org.quartz.simpl.RAMJobStore");
        return properties;
    }
}
