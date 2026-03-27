import type { User } from '../types'

export function CustomerList({ customers }: { customers: User[] }) {
  return (
    <article className="panel">
      <h2>Customers</h2>
      <div className="stack">
        {customers.map((customer) => (
          <div key={customer.id} className="listRow">
            <div>
              <strong>{customer.username}</strong>
              <p>{customer.email} / {customer.role}</p>
            </div>
            <span>{customer.address}</span>
          </div>
        ))}
      </div>
    </article>
  )
}
