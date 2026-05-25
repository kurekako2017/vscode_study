<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html>
<head>
    <title>My Cart</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
</head>
<body>
<div class="container mt-4">
    <h2>My Cart</h2>
    <c:if test="${not empty cartMsg}">
        <div class="alert alert-success">${cartMsg}</div>
    </c:if>
    <c:if test="${not empty msg}">
        <div class="alert alert-warning">${msg}</div>
    </c:if>
    <table class="table table-bordered">
        <thead>
        <tr>
            <th>Product Name</th>
            <th>Category</th>
            <th>Price</th>
            <th>Description</th>
            <th>Action</th>
        </tr>
        </thead>
        <tbody>
        <c:forEach var="product" items="${products}">
            <tr>
                <td>${product.name}</td>
                <td>${product.category.name}</td>
                <td>${product.price}</td>
                <td>${product.description}</td>
                <td>
                    <form action="/user/cart/delete" method="get" style="display:inline-block;">
                        <input type="hidden" name="id" value="${product.id}">
                        <button type="submit" class="btn btn-sm btn-danger">Delete</button>
                    </form>
                </td>
            </tr>
        </c:forEach>
        </tbody>
    </table>
    <a href="/user/products" class="btn btn-primary">Continue Shopping</a>
</div>
</body>
</html>
