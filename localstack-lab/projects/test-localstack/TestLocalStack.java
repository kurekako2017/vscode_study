import java.net.HttpURLConnection;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class TestLocalStack {
    public static void main(String[] args) {
        System.out.println("===== LocalStack 连接测试 =====\n");

        try {
            // 测试 LocalStack Health Endpoint
            String healthUrl = "http://localhost:4566/_localstack/health";
            System.out.println("测试 URL: " + healthUrl);

            URL url = new URL(healthUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setConnectTimeout(5000);
            conn.setReadTimeout(5000);

            int responseCode = conn.getResponseCode();
            System.out.println("响应码: " + responseCode);

            if (responseCode == 200) {
                BufferedReader in = new BufferedReader(
                    new InputStreamReader(conn.getInputStream())
                );
                String inputLine;
                StringBuilder response = new StringBuilder();

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();

                System.out.println("\n✓ LocalStack 运行正常！\n");
                System.out.println("健康状态响应:");
                System.out.println(response.toString());
            } else {
                System.out.println("\n✗ LocalStack 响应异常");
            }

        } catch (Exception e) {
            System.out.println("\n✗ 无法连接到 LocalStack");
            System.out.println("错误信息: " + e.getMessage());
            System.out.println("\n请确认:");
            System.out.println("1. Docker 正在运行");
            System.out.println("2. LocalStack 容器已启动: docker start localstack");
            System.out.println("3. 端口 4566 未被占用");
        }

        System.out.println("\n===== 测试完成 =====");
    }
}

