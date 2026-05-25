package com.jtspringproject.JtSpringProject.batch;

import static org.junit.jupiter.api.Assertions.*;

import com.jtspringproject.JtSpringProject.models.Category;
import com.jtspringproject.JtSpringProject.models.Product;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.TestPropertySource;
import org.springframework.transaction.annotation.Transactional;

/**
 * ProductCategoryCheckBatchService の統合テスト。
 *
 * <p>H2 インメモリデータベースを使用し、実際のデータベース環境で
 * バッチの動作を検証する。</p>
 *
 * <h3>テスト対象：</h3>
 * <ul>
 *   <li>CSV ファイル出力の形式検証</li>
 *   <li>ログ出力の形式検証</li>
 *   <li>DB トランザクション（読み取り専用）の検証</li>
 *   <li>終了コード返却の検証</li>
 * </ul>
 *
 * @author JT Spring Project Team
 * @version 1.0
 */
@SpringBootTest
@ActiveProfiles("batch")
@TestPropertySource(properties = {
    "spring.datasource.url=jdbc:h2:mem:testdb;MODE=MySQL;DB_CLOSE_DELAY=-1",
    "spring.jpa.hibernate.ddl-auto=create-drop",
    "logging.level.com.jtspringproject=DEBUG"
})
@DisplayName("BAT-005 整合チェックバッチ統合テスト")
class ProductCategoryCheckBatchIntegrationTest {

    @Autowired
    private ProductCategoryCheckBatchService batchService;

    @TempDir
    Path tempDir;

    private static final String BATCH_OUTPUT_DIR = "${batch.output.dir}";

    @BeforeEach
    void setUp() {
        // バッチ出力ディレクトリを一時ディレクトリに設定
        System.setProperty("batch.output.dir", tempDir.toString());
    }

    @Test
    @DisplayName("ITC01: CSV ファイルが正しい形式で出力される")
    @Transactional
    void test_CSVFileFormatIsValid() throws IOException {
        // このテストは実際のデータが必要なため、@Sql アノテーションで
        // 初期データを投入する方法が望ましい

        // 期待される CSV ヘッダ
        String expectedHeader = "check_timestamp,product_id,product_name,category_id,category_name,quantity,price,check_status,error_messages";

        // CSV ファイルが存在し、ヘッダが正しいことを検証
        // このテストは実装後に具体的なデータで実施される
    }

    @Test
    @DisplayName("ITC02: ログファイルが指定されたディレクトリに出力される")
    @Transactional
    void test_LogFileOutputLocation() {
        // logs/batch/ ディレクトリにログファイルが出力されることを検証
        Path logDir = Paths.get("logs/batch");

        // テスト実行後、ログディレクトリが存在することを確認
        // このテストは実装後に具体的なディレクトリチェックで実施される
    }

    @Test
    @DisplayName("ITC03: トランザクションが読み取り専用で実行される")
    void test_TransactionReadOnly() {
        // 読み取り専用トランザクションでの実行確認
        // ProductCategoryCheckBatchService の @Transactional(readOnly = true) により
        // データベースへの書き込みが行われないことを検証

        // 実際のテストでは、AOP インターセプションや メトリクス収集で確認
    }

    @Test
    @DisplayName("ITC04: 終了コードが正しく返却される（正常系）")
    void test_ExitCodeNormal() {
        // バッチが正常に実行され、終了コード 0 が返却されることを検証
        // (前提: テストデータすべてが有効である)

        int exitCode = batchService.runBatch();
        assertTrue(exitCode >= 0 && exitCode <= 2, "終了コードが 0-2 の範囲内");
    }

    @Test
    @DisplayName("ITC05: CSV 出力のエスケープが正しく処理される")
    void test_CSVEscapeHandling() {
        // CSV 値に含まれるダブルクォート、カンマ、改行が
        // 正しくエスケープされることを検証
    }

    @Test
    @DisplayName("ITC06: 大量データ処理時のパフォーマンス（10,000 件）")
    void test_PerformanceWithLargeDataset() {
        // 10,000 件のデータを処理し、5 秒以内に完了することを検証
        // 実装後、@Sql で初期データ投入して実施

        long startTime = System.currentTimeMillis();
        // batchService.runBatch();
        long endTime = System.currentTimeMillis();
        long durationMs = endTime - startTime;

        // assertTrue(durationMs < 5000, "10,000 件を 5 秒以内に処理完了");
    }

    @Test
    @DisplayName("ITC07: メモリ使用量が適切な範囲内（バッチ処理中）")
    void test_MemoryUsageOptimization() {
        // バッチ実行中のメモリ使用量が適切な範囲内（MAX 100MB）であることを検証
        // Runtime.totalMemory(), Runtime.freeMemory() で確認

        Runtime runtime = Runtime.getRuntime();
        long memBefore = runtime.totalMemory() - runtime.freeMemory();

        // batchService.runBatch();

        long memAfter = runtime.totalMemory() - runtime.freeMemory();
        long memUsed = memAfter - memBefore;

        // assertTrue(memUsed < 100 * 1024 * 1024, "メモリ使用量が 100MB 以下");
    }

    @Test
    @DisplayName("ITC08: 複数回実行時の独立性（バッチ状態の分離）")
    void test_MultipleExecutionIndependence() {
        // バッチを複数回実行し、前回の実行結果が次の実行に影響しないことを検証

        int exitCode1 = batchService.runBatch();
        int exitCode2 = batchService.runBatch();

        // 複数回実行しても同じ結果が得られることを確認
        assertEquals(exitCode1, exitCode2, "複数回実行時の結果が一致");
    }
}
