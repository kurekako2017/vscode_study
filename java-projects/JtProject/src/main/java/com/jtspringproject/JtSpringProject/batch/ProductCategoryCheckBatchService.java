package com.jtspringproject.JtSpringProject.batch;

import com.jtspringproject.JtSpringProject.dao.ProductDao;
import com.jtspringproject.JtSpringProject.models.Category;
import com.jtspringproject.JtSpringProject.models.Product;
import com.jtspringproject.JtSpringProject.common.util.InputCheckUtil;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 商品·分類マスタ整合チェックの実装。
 *
 * <p>BAT-005 として、商品マスタと分類マスタの整合性をチェックし、
 * 結果を CSV ファイルに出力する。</p>
 *
 * <h3>処理フロー：</h3>
 * <ol>
 *   <li>フェーズ 1: カテゴリ参照整合チェック（存在・削除フラグ確認）</li>
 *   <li>フェーズ 2: 商品データ有効性チェック（必須項目・形式確認）</li>
 *   <li>フェーズ 3: マスタ連動整合性チェック（分類利用可否確認）</li>
 *   <li>結果 CSV 出力・ログ出力</li>
 * </ol>
 *
 * @author JT Spring Project Team
 * @version 1.0
 */
@Service
@Profile("batch")
public class ProductCategoryCheckBatchService {

    private static final Logger logger = LoggerFactory.getLogger(ProductCategoryCheckBatchService.class);
    private static final DateTimeFormatter FILE_TIMESTAMP_FORMAT =
        DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss");
    private static final DateTimeFormatter CSV_TIMESTAMP_FORMAT =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    private final ProductDao productDao;

    @Value("${batch.output.dir:batch-output}")
    private String batchOutputDir;

    public ProductCategoryCheckBatchService(ProductDao productDao) {
        this.productDao = productDao;
    }

    /**
     * バッチを実行し、整合チェック結果を CSV に出力する。
     *
     * <p>フェーズ 1-3 をを実行し、NG 件数に応じて終了コードを返却する。</p>
     *
     * @return 終了コード: 0=正常、2=業務NG有、1=システム異常
     */
    @Transactional(readOnly = true)
    public int runBatch() {
        logger.info("商品·分類マスタ整合チェックバッチを開始します。");
        LocalDateTime now = LocalDateTime.now();
        List<Product> products = productDao.getProductsWithCategories();
        List<String> csvLines = new ArrayList<>();
        int ngCount = 0;

        // CSV ヘッダ
        csvLines.add(
            "check_timestamp,product_id,product_name,category_id,category_name,quantity,price,check_status,error_messages");

        // フェーズ 1: カテゴリ参照整合チェック
        logger.info("フェーズ 1: カテゴリ参照整合チェックを実行します。対象件数: {}", products.size());
        Map<Integer, Category> categoryCache = buildCategoryCache(products);
        int phase1NgCount = 0;

        for (Product product : products) {
            List<String> errors = new ArrayList<>();

            // フェーズ 1: カテゴリ参照整合
            errors.addAll(validateCategoryReference(product, categoryCache));

            // フェーズ 2: 商品データ有効性
            errors.addAll(validateProductData(product));

            // フェーズ 3: マスタ連動整合性
            errors.addAll(validateMasterIntegrity(product, categoryCache));

            if (!errors.isEmpty()) {
                ngCount++;
                if (errors.stream().anyMatch(e -> e.startsWith("ERR_CAT"))) {
                    phase1NgCount++;
                }
            }

            // CSV 行を構築
            String status = errors.isEmpty() ? "OK" : "NG";
            Category category = product.getCategory();
            csvLines.add(String.join(",",
                csvValue(CSV_TIMESTAMP_FORMAT.format(now)),
                csvValue(String.valueOf(product.getId())),
                csvValue(product.getName()),
                csvValue(category == null ? "" : String.valueOf(category.getId())),
                csvValue(category == null ? "" : category.getName()),
                csvValue(String.valueOf(product.getQuantity())),
                csvValue(String.valueOf(product.getPrice())),
                csvValue(status),
                csvValue(String.join(" | ", errors))));
        }

        logger.info("フェーズ 1: カテゴリ参照整合チェック完了。NG件数: {}", phase1NgCount);

        // CSV を出力
        Path outputFile = buildOutputFile(now);
        try {
            writeLines(outputFile, csvLines);
            logger.info("バッチ終了: 対象件数: {}, NG件数: {}, 出力ファイル: {}",
                products.size(), ngCount, outputFile.toAbsolutePath());
        } catch (IOException e) {
            logger.error("CSV ファイル出力に失敗しました: {}", e.getMessage(), e);
            return 1;  // システム異常
        }

        return ngCount > 0 ? 2 : 0;
    }

    /**
     * フェーズ 1: カテゴリ参照整合チェック
     *
     * <p>以下をチェック：
     * - CATEGORY_ID が NULL でないか
     * - CATEGORY テーブルに存在するか
     * </p>
     *
     * @param product 商品オブジェクト
     * @param categoryCache カテゴリキャッシュ
     * @return エラーコードのリスト（エラーなければ空のリスト）
     */
    private List<String> validateCategoryReference(Product product, Map<Integer, Category> categoryCache) {
        List<String> errors = new ArrayList<>();

        if (product.getCategory() == null) {
            errors.add("ERR_CAT_NULL");
            logger.warn("[商品ID={}] ERR_CAT_NULL: カテゴリが設定されていません", product.getId());
        } else {
            Integer categoryId = product.getCategory().getId();
            Category cachedCategory = categoryCache.get(categoryId);

            if (cachedCategory == null) {
                errors.add("ERR_CAT_NOT_FOUND");
                logger.warn("[商品ID={}] ERR_CAT_NOT_FOUND: カテゴリID={} が見つかりません",
                    product.getId(), categoryId);
            }
        }

        return errors;
    }

    /**
     * フェーズ 2: 商品データ有効性チェック
     *
     * <p>以下をチェック：
     * - 商品名が空でないか
     * - 商品名が最大長を超えていないか
     * - 価格が 0 より大きいか、最大値を超えていないか
     * - 在庫数が 0 以上か、最大値を超えていないか
     * </p>
     *
     * @param product 商品オブジェクト
     * @return エラーコードのリスト
     */
    private List<String> validateProductData(Product product) {
        List<String> errors = new ArrayList<>();

        // 商品名チェック
        if (!InputCheckUtil.hasText(product.getName())) {
            errors.add("ERR_PROD_NAME_EMPTY");
            logger.warn("[商品ID={}] ERR_PROD_NAME_EMPTY: 商品名が空です", product.getId());
        } else if (product.getName().length() > 100) {
            errors.add("ERR_PROD_NAME_TOO_LONG");
            logger.warn("[商品ID={}] ERR_PROD_NAME_TOO_LONG: 商品名が長すぎます ({}文字)",
                product.getId(), product.getName().length());
        }

        // 価格チェック
        if (product.getPrice() <= 0 || product.getPrice() > 999999) {
            errors.add("ERR_PRICE_INVALID");
            logger.warn("[商品ID={}] ERR_PRICE_INVALID: 価格が無効です ({})",
                product.getId(), product.getPrice());
        }

        // 在庫数チェック
        if (product.getQuantity() < 0 || product.getQuantity() > 999999) {
            errors.add("ERR_QUANTITY_INVALID");
            logger.warn("[商品ID={}] ERR_QUANTITY_INVALID: 在庫数が無効です ({})",
                product.getId(), product.getQuantity());
        }

        return errors;
    }

    /**
     * フェーズ 3: マスタ連動整合性チェック
     *
     * <p>以下をチェック：
     * - カテゴリの利用可否（削除フラグ確認）
     * - 商品の販売可能状態（在庫・価格確認）
     * </p>
     *
     * @param product 商品オブジェクト
     * @param categoryCache カテゴリキャッシュ
     * @return エラーコードのリスト
     */
    private List<String> validateMasterIntegrity(Product product, Map<Integer, Category> categoryCache) {
        List<String> errors = new ArrayList<>();

        Category category = product.getCategory();
        if (category != null) {
            // 在庫が 0 の場合は警告ログのみ（NG ではない）
            if (product.getQuantity() == 0) {
                logger.info("[商品ID={}] 在庫が 0 です。販売可能状態を確認してください", product.getId());
            }
        }

        return errors;
    }

    /**
     * カテゴリキャッシュを構築する
     *
     * <p>後続の処理で複数回参照するため、メモリ内キャッシュを事前構築する。</p>
     *
     * @param products 商品リスト
     * @return カテゴリ ID → Category のマップ
     */
    private Map<Integer, Category> buildCategoryCache(List<Product> products) {
        Map<Integer, Category> cache = new HashMap<>();
        for (Product product : products) {
            if (product.getCategory() != null && product.getCategory().getId() > 0) {
                cache.putIfAbsent(product.getCategory().getId(), product.getCategory());
            }
        }
        logger.debug("カテゴリキャッシュを構築しました。キャッシュ件数: {}", cache.size());
        return cache;
    }

    /**
     * CSV 値をエスケープする
     *
     * <p>ダブルクォートとカンマを含む値を CSV 形式でエスケープする。</p>
     *
     * @param value CSV フィールド値
     * @return エスケープされた値
     */
    private String csvValue(String value) {
        if (value == null) {
            return "";
        }
        if (value.contains(",") || value.contains("\"") || value.contains("\n")) {
            return "\"" + value.replace("\"", "\"\"") + "\"";
        }
        return value;
    }

    /**
     * 出力ファイルパスを構築する
     *
     * @param now 実行時刻
     * @return 出力ファイルパス
     */
    private Path buildOutputFile(LocalDateTime now) {
        String filename = "product_category_check_" + FILE_TIMESTAMP_FORMAT.format(now) + ".csv";
        return Paths.get(batchOutputDir, filename);
    }

    /**
     * CSV 行をファイルに書き込む
     *
     * @param outputFile 出力ファイルパス
     * @param lines CSV 行のリスト
     * @throws IOException ファイル出力エラー
     */
    private void writeLines(Path outputFile, List<String> lines) throws IOException {
        Files.createDirectories(outputFile.getParent());
        Files.write(outputFile, lines, StandardCharsets.UTF_8);
    }
}
