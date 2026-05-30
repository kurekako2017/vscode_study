package com.jtspringproject.JtSpringProject.batch.service;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Profile;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * BAT-006 カート残留データ棚卸バッチ本体。
 *
 * <p>概要: カートに紐づく `CART_PRODUCT` が存在しないカート（未使用カート）や、
 * `CART_PRODUCT` 側で参照先が存在しない孤立レコード（オーファン）を収集し、CSV 出力する。
 * オプションで検出した不要リンクや空カートを削除する機能を持つ（`batch.cart-residual.delete`）。
 *
 * <p>出力項目: 実行タイムスタンプ、レコード種別、cart_id、customer_id、cart_product_id、product_id、ステータス、メッセージ
 *
 * <p>関連設計書: doc/jp-docs/03_database/89_カート残留データ棚卸詳細設計書.md
 */
@Service
@Profile("batch")
public class CartResidualInventoryBatchService {

    private static final Logger logger = LoggerFactory.getLogger(CartResidualInventoryBatchService.class);
    private static final DateTimeFormatter FILE_TIMESTAMP_FORMAT =
        DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss");
    private static final DateTimeFormatter CSV_TIMESTAMP_FORMAT =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    private final JdbcTemplate jdbcTemplate;

    @Value("${batch.output.dir:batch-output}")
    private String batchOutputDir;

    @Value("${batch.cart-residual.delete:false}")
    private boolean deleteMode;

    public CartResidualInventoryBatchService(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    /**
     * バッチを実行する。
     *
     * @return 終了コード
     */
    @Transactional
    public int runBatch() {
        logger.info("BAT-006 カート残留データ棚卸を開始します。deleteMode={}", deleteMode);
        LocalDateTime now = LocalDateTime.now();
        try {
            List<Map<String, Object>> emptyCarts = queryEmptyCarts();
            List<Map<String, Object>> orphanLinks = queryOrphanCartProducts();

            Path output = buildOutputFile(now);
            writeCsv(output, now, emptyCarts, orphanLinks);

            if (deleteMode) {
                int deletedLinks = deleteOrphanLinks();
                int deletedCarts = deleteEmptyCarts();
                logger.info("BAT-006 削除モードで実行しました。削除件数: cart_product={}, cart={}",
                    deletedLinks, deletedCarts);
            }

            int ngCount = emptyCarts.size() + orphanLinks.size();
            logger.info("BAT-006 が完了しました。残留件数: {}, 出力ファイル: {}",
                ngCount, output.toAbsolutePath());
            return ngCount > 0 ? 2 : 0;
        } catch (Exception exception) {
            logger.error("BAT-006 の実行中にエラーが発生しました。", exception);
            return 1;
        }
    }

    private List<Map<String, Object>> queryEmptyCarts() {
        String sql =
            "SELECT c.id AS cart_id, c.customer_id AS customer_id "
                + "FROM CART c "
                + "LEFT JOIN CART_PRODUCT cp ON cp.cart_id = c.id "
                + "WHERE cp.id IS NULL "
                + "ORDER BY c.id";
        return jdbcTemplate.queryForList(sql);
    }

    private List<Map<String, Object>> queryOrphanCartProducts() {
        String sql =
            "SELECT cp.id AS cart_product_id, cp.cart_id, cp.product_id, "
                + "CASE WHEN c.id IS NULL THEN 'CART_MISSING' ELSE '' END AS cart_status, "
                + "CASE WHEN p.product_id IS NULL THEN 'PRODUCT_MISSING' ELSE '' END AS product_status "
                + "FROM CART_PRODUCT cp "
                + "LEFT JOIN CART c ON cp.cart_id = c.id "
                + "LEFT JOIN PRODUCT p ON cp.product_id = p.product_id "
                + "WHERE c.id IS NULL OR p.product_id IS NULL "
                + "ORDER BY cp.id";
        return jdbcTemplate.queryForList(sql);
    }

    private int deleteOrphanLinks() {
        String sql =
            "DELETE FROM CART_PRODUCT "
                + "WHERE cart_id NOT IN (SELECT id FROM CART) "
                + "OR product_id NOT IN (SELECT product_id FROM PRODUCT)";
        return jdbcTemplate.update(sql);
    }

    private int deleteEmptyCarts() {
        String sql =
            "DELETE FROM CART WHERE id NOT IN (SELECT DISTINCT cart_id FROM CART_PRODUCT)";
        return jdbcTemplate.update(sql);
    }

    private Path buildOutputFile(LocalDateTime now) {
        String filename = "cart_residual_inventory_" + FILE_TIMESTAMP_FORMAT.format(now) + ".csv";
        return Paths.get(batchOutputDir, filename);
    }

    private void writeCsv(
        Path output,
        LocalDateTime now,
        List<Map<String, Object>> emptyCarts,
        List<Map<String, Object>> orphanLinks) throws IOException {

        List<String> lines = new ArrayList<>();
        lines.add("check_timestamp,record_type,cart_id,customer_id,cart_product_id,product_id,status,messages");

        for (Map<String, Object> row : emptyCarts) {
            lines.add(String.join(",",
                csv(CSV_TIMESTAMP_FORMAT.format(now)),
                csv("EMPTY_CART"),
                csv(String.valueOf(row.get("cart_id"))),
                csv(String.valueOf(row.get("customer_id"))),
                csv(""),
                csv(""),
                csv("NG"),
                csv("CART_HAS_NO_PRODUCTS")));
        }

        for (Map<String, Object> row : orphanLinks) {
            String cartStatus = String.valueOf(row.get("cart_status"));
            String productStatus = String.valueOf(row.get("product_status"));
            String msg = (cartStatus + " " + productStatus).trim();
            lines.add(String.join(",",
                csv(CSV_TIMESTAMP_FORMAT.format(now)),
                csv("ORPHAN_CART_PRODUCT"),
                csv(String.valueOf(row.get("cart_id"))),
                csv(""),
                csv(String.valueOf(row.get("cart_product_id"))),
                csv(String.valueOf(row.get("product_id"))),
                csv("NG"),
                csv(msg)));
        }

        Files.createDirectories(output.getParent());
        Files.write(output, lines, StandardCharsets.UTF_8);
    }

    private String csv(String value) {
        if (value == null || "null".equalsIgnoreCase(value)) {
            return "";
        }
        if (value.contains(",") || value.contains("\"") || value.contains("\n")) {
            return "\"" + value.replace("\"", "\"\"") + "\"";
        }
        return value;
    }
}
