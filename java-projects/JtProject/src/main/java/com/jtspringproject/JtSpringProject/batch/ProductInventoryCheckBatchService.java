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
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 商品在庫整合チェックの模擬バッチ本体（BAT-LAB-001）。
 *
 * <p>学習用の最小構成バッチとして、商品データの整合性をチェックし、
 * 結果を CSV ファイルに出力する。</p>
 *
 * <h3>処理フロー：</h3>
 * <ol>
 *   <li>商品一覧を取得</li>
 *   <li>商品ごとに整合チェック実施</li>
 *   <li>結果を CSV に出力</li>
 *   <li>ログへ件数を出力</li>
 *   <li>終了コードを返却</li>
 * </ol>
 *
 * @author JT Spring Project Team
 * @version 1.0
 */
@Service
@Profile("batch")
public class ProductInventoryCheckBatchService {

    private static final Logger logger = LoggerFactory.getLogger(ProductInventoryCheckBatchService.class);
    private static final DateTimeFormatter FILE_TIMESTAMP_FORMAT =
        DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss");
    private static final DateTimeFormatter CSV_TIMESTAMP_FORMAT =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    private final ProductDao productDao;

    @Value("${batch.output.dir:batch-output}")
    private String batchOutputDir;

    public ProductInventoryCheckBatchService(ProductDao productDao) {
        this.productDao = productDao;
    }

    /**
     * バッチを実行し、結果 CSV を出力する。
     *
     * @return 終了コード
     */
    @Transactional(readOnly = true)
    public int runBatch() {
        LocalDateTime now = LocalDateTime.now();
        List<Product> products = productDao.getProducts();
        List<String> lines = new ArrayList<>();
        int ngCount = 0;

        lines.add(
            "check_timestamp,product_id,product_name,category_id,category_name,quantity,price,status,check_messages");

        for (Product product : products) {
            List<String> messages = validateProduct(product);
            String status = messages.isEmpty() ? "OK" : "NG";
            if (!messages.isEmpty()) {
                ngCount++;
            }

            Category category = product.getCategory();
            lines.add(String.join(",",
                csv(CSV_TIMESTAMP_FORMAT.format(now)),
                csv(String.valueOf(product.getId())),
                csv(product.getName()),
                csv(category == null ? "" : String.valueOf(category.getId())),
                csv(category == null ? "" : category.getName()),
                csv(String.valueOf(product.getQuantity())),
                csv(String.valueOf(product.getPrice())),
                csv(status),
                csv(String.join(" | ", messages))));
        }

        Path outputFile = buildOutputFile(now);
        writeLines(outputFile, lines);

        logger.info("商品在庫整合チェックバッチを終了しました。対象件数: {}, NG件数: {}, 出力ファイル: {}",
            products.size(), ngCount, outputFile.toAbsolutePath());
        return ngCount > 0 ? 2 : 0;
    }

    private List<String> validateProduct(Product product) {
        List<String> messages = new ArrayList<>();

        if (!InputCheckUtil.hasText(product.getName())) {
            messages.add("PRODUCT_NAME_EMPTY");
        }
        if (product.getCategory() == null) {
            messages.add("CATEGORY_MISSING");
        }
        if (product.getQuantity() < 0) {
            messages.add("NEGATIVE_QUANTITY");
        }
        if (product.getPrice() <= 0) {
            messages.add("INVALID_PRICE");
        }

        return messages;
    }

    private Path buildOutputFile(LocalDateTime now) {
        String fileName = "product_inventory_check_" + FILE_TIMESTAMP_FORMAT.format(now) + ".csv";
        return Paths.get(batchOutputDir, fileName);
    }

    private void writeLines(Path outputFile, List<String> lines) {
        try {
            Files.createDirectories(outputFile.getParent());
            Files.write(outputFile, lines, StandardCharsets.UTF_8);
        } catch (IOException exception) {
            throw new IllegalStateException("バッチ結果 CSV の出力に失敗しました。", exception);
        }
    }

    private String csv(String value) {
        if (value == null) {
            return "\"\"";
        }
        String escaped = value.replace("\"", "\"\"");
        return "\"" + escaped + "\"";
    }
}
