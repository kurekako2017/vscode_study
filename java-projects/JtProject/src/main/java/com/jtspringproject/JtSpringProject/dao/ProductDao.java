package com.jtspringproject.JtSpringProject.dao;

import com.jtspringproject.JtSpringProject.models.Product;
import java.util.List;

/**
 * 商品データアクセスインタフェース / Product DAO
 *
 * <p>商品に関する DB 操作を抽象化したインタフェース。バッチ処理やサービス層はこのインタフェースを通じて
 * 商品データを取得・更新する。
 *
 * <p>実装クラス: com.jtspringproject.JtSpringProject.dao.impl.ProductDaoImpl
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see com.jtspringproject.JtSpringProject.dao.impl.ProductDaoImpl
 */
public interface ProductDao {

    /**
     * 获取所有商品。
     *
     * <p>バッチやサービスで使用するための全件取得。返却される Product は必要に応じて Category を含む可能性がある。
     * 実装によってはページングや条件追加が考慮される。
     *
     * @return 商品列表
     */
    List<Product> getProducts();

    /**
     * 添加商品
     * @param product 商品对象
     * @return 添加后的商品
     */
    Product addProduct(Product product);

    /**
     * 根据ID获取商品
     * @param id 商品ID
     * @return 商品对象
     */
    Product getProduct(int id);

    /**
     * 更新商品
     * @param product 要更新的商品
     * @return 更新后的商品
     */
    Product updateProduct(Product product);

    /**
     * 删除商品
     * @param id 商品ID
     * @return 是否删除成功
     */
    Boolean deletProduct(int id);

    /**
     * 获取所有商品（包含分类信息），用于整合チェックバッチ処理。
     *
     * <p>このメソッドは商品とカテゴリ情報を結合して返却する。バッチの整合チェック
     *（例: `ProductCategoryCheckBatchService`）から利用されることを想定している。
     * 実装は LEFT JOIN 相当のクエリを使用し、カテゴリが存在しない商品も検出可能にする。
     *
     * @return 商品リスト（分類情報付き）
     */
    List<Product> getProductsWithCategories();
}

