package com.jtspringproject.JtSpringProject.batch;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import com.jtspringproject.JtSpringProject.dao.ProductDao;
import com.jtspringproject.JtSpringProject.models.Category;
import com.jtspringproject.JtSpringProject.models.Product;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.test.util.ReflectionTestUtils;

/**
 * ProductCategoryCheckBatchService のユニットテスト。
 *
 * <p>フェーズ 1-3 のチェックロジック、CSV 出力、終了コード返却を検証する。</p>
 *
 * @author JT Spring Project Team
 * @version 1.0
 */
@DisplayName("BAT-005 商品·分類マスタ整合チェックバッチ")
class ProductCategoryCheckBatchServiceTest {

    @Mock
    private ProductDao productDao;

    private ProductCategoryCheckBatchService batchService;

    @TempDir
    Path tempDir;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        batchService = new ProductCategoryCheckBatchService(productDao);
        ReflectionTestUtils.setField(batchService, "batchOutputDir", tempDir.toString());
    }

    // ========== フェーズ 1: カテゴリ参照整合チェック ==========

    @Test
    @DisplayName("TC01: カテゴリが存在し、DELETE_FLG = 0 の場合、OK と判定される")
    void test_CategoryFound_OK() {
        // Arrange
        Category category = new Category();
        category.setId(101);
        category.setName("果物");

        Product product = new Product();
        product.setId(1001);
        product.setName("アップル");
        product.setCategory(category);
        product.setQuantity(500);
        product.setPrice(15000);

        when(productDao.getProductsWithCategories()).thenReturn(List.of(product));

        // Act
        int exitCode = batchService.runBatch();

        // Assert
        assertEquals(0, exitCode, "カテゴリが存在し、DELETE_FLG = 0 の場合、終了コード 0 が返される");
    }

    @Test
    @DisplayName("TC02: カテゴリが存在しない場合、ERR_CAT_NOT_FOUND と判定される")
    void test_CategoryNotFound_NG() {
        // Arrange
        Category category = new Category();
        category.setId(999);  // 存在しないカテゴリ

        Product product = new Product();
        product.setId(1002);
        product.setName("バナナ");
        product.setCategory(category);
        product.setQuantity(100);
        product.setPrice(8000);

        when(productDao.getProductsWithCategories()).thenReturn(List.of(product));

        // Act
        int exitCode = batchService.runBatch();

        // Assert
        assertEquals(2, exitCode, "カテゴリが存在しない場合、終了コード 2（業務NG）が返される");
    }

    @Test
    @DisplayName("TC03: カテゴリが DELETE_FLG = 1（削除済み）の場合、ERR_CAT_DELETED と判定される")
    void test_CategoryDeleted_NG() {
        // Arrange
        Category category = new Category();
        category.setId(102);
        category.setName("野菜");
        category.setDeleteFlg(1);  // 削除済み

        Product product = new Product();
        product.setId(1003);
        product.setName("ニンジン");
        product.setCategory(category);
        product.setQuantity(200);
        product.setPrice(12000);

        when(productDao.getProductsWithCategories()).thenReturn(List.of(product));

        // Act
        int exitCode = batchService.runBatch();

        // Assert
        assertEquals(2, exitCode, "カテゴリが削除済みの場合、終了コード 2（業務NG）が返される");
    }

    @Test
    @DisplayName("TC04: カテゴリが NULL の場合、ERR_CAT_NULL と判定される")
    void test_CategoryNull_NG() {
        // Arrange
        Product product = new Product();
        product.setId(1004);
        product.setName("トマト");
        product.setCategory(null);  // NULL
        product.setQuantity(150);
        product.setPrice(10000);

        when(productDao.getProductsWithCategories()).thenReturn(List.of(product));

        // Act
        int exitCode = batchService.runBatch();

        // Assert
        assertEquals(2, exitCode, "カテゴリが NULL の場合、終了コード 2（業務NG）が返される");
    }

    // ========== フェーズ 2: 商品データ有効性チェック ==========

    @Test
    @DisplayName("TC05: 商品名が空の場合、ERR_PROD_NAME_EMPTY と判定される")
    void test_ProductNameEmpty_NG() {
        // Arrange
        Category category = new Category();
        category.setId(101);
        category.setName("果物");
        category.setDeleteFlg(0);

        Product product = new Product();
        product.setId(1005);
        product.setName("");  // 空
        product.setCategory(category);
        product.setQuantity(100);
        product.setPrice(100.00);
        product.setDeleteFlg(false);

        when(productDao.getProductsWithCategories()).thenReturn(List.of(product));

        // Act
        int exitCode = batchService.runBatch();

        // Assert
        assertEquals(2, exitCode, "商品名が空の場合、終了コード 2（業務NG）が返される");
    }

    @Test
    @DisplayName("TC06: 商品名が 100 文字を超える場合、ERR_PROD_NAME_TOO_LONG と判定される")
    void test_ProductNameTooLong_NG() {
        // Arrange
        Category category = new Category();
        category.setId(101);
        category.setName("果物");
        category.setDeleteFlg(0);

        Product product = new Product();
        product.setId(1006);
        product.setName("a".repeat(101));  // 101文字（超過）
        product.setCategory(category);
        product.setQuantity(100);
        product.setPrice(100.00);
        product.setDeleteFlg(false);

        when(productDao.getProductsWithCategories()).thenReturn(List.of(product));

        // Act
        int exitCode = batchService.runBatch();

        // Assert
        assertEquals(2, exitCode, "商品名が 100 文字を超える場合、終了コード 2（業務NG）が返される");
    }

    @Test
    @DisplayName("TC07: 価格が 0 以下の場合、ERR_PRICE_INVALID と判定される")
    void test_PriceInvalid_NG() {
        // Arrange
        Category category = new Category();
        category.setId(101);
        category.setName("果物");
        category.setDeleteFlg(0);

        Product product = new Product();
        product.setId(1007);
        product.setName("グレープ");
        product.setCategory(category);
        product.setQuantity(100);
        product.setPrice(0.00);  // 無効
        product.setDeleteFlg(false);

        when(productDao.getProductsWithCategories()).thenReturn(List.of(product));

        // Act
        int exitCode = batchService.runBatch();

        // Assert
        assertEquals(2, exitCode, "価格が 0 以下の場合、終了コード 2（業務NG）が返される");
    }

    @Test
    @DisplayName("TC08: 在庫数が負数の場合、ERR_QUANTITY_INVALID と判定される")
    void test_QuantityNegative_NG() {
        // Arrange
        Category category = new Category();
        category.setId(101);
        category.setName("果物");
        category.setDeleteFlg(0);

        Product product = new Product();
        product.setId(1008);
        product.setName("オレンジ");
        product.setCategory(category);
        product.setQuantity(-10);  // 負数
        product.setPrice(12000);

        when(productDao.getProductsWithCategories()).thenReturn(List.of(product));

        // Act
        int exitCode = batchService.runBatch();

        // Assert
        assertEquals(2, exitCode, "在庫数が負数の場合、終了コード 2（業務NG）が返される");
    }

    // ========== 複合テスト ==========

    @Test
    @DisplayName("TC09: 複数のエラーがある場合、すべてのエラーが CSV に記録される")
    void test_MultipleErrors_AllRecorded() throws IOException {
        // Arrange
        Product product1 = new Product();
        product1.setId(1001);
        product1.setName("");  // エラー1: 商品名が空
        product1.setCategory(null);  // エラー2: カテゴリNULL
        product1.setQuantity(100);
        product.setPrice(10000);

        Product product2 = new Product();
        product2.setId(1002);
        product2.setName("有効な商品");
        Category category = new Category();
        category.setId(101);
        category.setName("果物");
        product2.setCategory(category);
        product2.setQuantity(50);
        product2.setPrice(15000);

        when(productDao.getProductsWithCategories()).thenReturn(List.of(product1, product2));

        // Act
        int exitCode = batchService.runBatch();

        // Assert
        assertEquals(2, exitCode, "エラーがある場合、終了コード 2 が返される");

        // CSV ファイルを検証
        Path csvFile = tempDir.resolve("product_category_check_" + java.time.LocalDateTime.now().format(
            java.time.format.DateTimeFormatter.ofPattern("yyyyMMdd")) + "*.csv");
        List<Path> csvFiles = new ArrayList<>();
        Files.walk(tempDir, 1)
            .filter(p -> p.toString().contains("product_category_check_"))
            .forEach(csvFiles::add);

        assertFalse(csvFiles.isEmpty(), "CSV ファイルが出力されている");

        String csvContent = Files.readString(csvFiles.get(0));
        assertTrue(csvContent.contains("ERR_PROD_NAME_EMPTY"), "ERR_PROD_NAME_EMPTY が記録されている");
        assertTrue(csvContent.contains("ERR_CAT_NULL"), "ERR_CAT_NULL が記録されている");
    }

    @Test
    @DisplayName("TC10: エラーがない場合、終了コード 0 が返される")
    void test_AllOK_ExitCode0() {
        // Arrange
        Category category = new Category();
        category.setId(101);
        category.setName("果物");
        category.setDeleteFlg(0);

        Product product = new Product();
        product.setId(1001);
        product.setName("アップル");
        product.setCategory(category);
        product.setQuantity(500);
        product.setPrice(150.00);
        product.setDeleteFlg(false);

        when(productDao.getProductsWithCategories()).thenReturn(List.of(product));

        // Act
        int exitCode = batchService.runBatch();

        // Assert
        assertEquals(0, exitCode, "エラーがない場合、終了コード 0 が返される");
    }

    @Test
    @DisplayName("TC11: 空のデータセットの場合、終了コード 0 が返される")
    void test_EmptyDataset_ExitCode0() {
        // Arrange
        when(productDao.getProductsWithCategories()).thenReturn(new ArrayList<>());

        // Act
        int exitCode = batchService.runBatch();

        // Assert
        assertEquals(0, exitCode, "データがない場合、終了コード 0 が返される");
    }
}
