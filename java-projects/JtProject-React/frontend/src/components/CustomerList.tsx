// 文件说明：
// 客户/用户列表组件，用于后台查看用户信息（用户名 / 邮箱 / 权限等）。
// 学习点：在列表渲染时确保每一项有唯一的 `key`，以提升渲染性能。
// 对应 JSP：displayCustomers.jsp
import type { User } from '../types'

export function CustomerList({ customers }: { customers: User[] }) {
  return (
    <article className="panel">
      <h2>Customers</h2>
      <div className="stack">
        {customers.map((customer) => (
          <div key={customer.id} className="listRow">
            <div>
                {/* 对应 displayCustomers.jsp 中的表格行片段：
                    <c:forEach var="customer" items="${customers}">
                      <tr>
                        <td>${customer.username}</td>
                        <td>${customer.email}</td>
                        <td>${customer.address}</td>
                      </tr>
                    </c:forEach>
                */}
                <strong>{customer.username}</strong>
                <p>{customer.email} / {customer.role}</p>
              </div>
              {/* 对应 displayCustomers.jsp 中的 <td>${customer.address}</td> */}
              <span>{customer.address}</span>
          </div>
        ))}
      </div>
    </article>
  )
}
