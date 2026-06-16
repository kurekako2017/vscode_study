// 最终结果很多时候是 Markdown，所以这里统一负责渲染。
// 这样后端只需要返回普通 Markdown 文本，前端就能显示标题、表格、链接等效果。
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface MarkdownRendererProps {
  content: string;
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  return (
    <div className="markdown-body">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a({ children, href, ...props }) {
            // 所有外链默认新开窗口，避免用户点走后把当前调试页面覆盖掉。
            return (
              <a href={href} rel="noreferrer" target="_blank" {...props}>
                {children}
              </a>
            );
          }
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
