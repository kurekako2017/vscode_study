<?php
/*
Plugin Name: AI Codex Agent
Description: 示例插件 —— 在后台通过 OpenAI 生成文章草稿，并提供 REST 接口供集成调用。
Version: 0.1.0
Author: vscode_study
Text Domain: ai-codex-agent
*/

if (!defined('ABSPATH')) exit;

class AICodexAgent {
    public function __construct(){
        add_action('admin_menu', [$this, 'add_admin_page']);
        add_action('rest_api_init', [$this, 'register_routes']);
    }

    public function add_admin_page(){
        add_menu_page('AI Codex', 'AI Codex', 'manage_options', 'ai-codex', [$this, 'admin_page']);
    }

    public function admin_page(){
        if (!current_user_can('manage_options')) return;
        echo '<div class="wrap"><h1>AI Codex Agent</h1>';
        if (isset($_POST['ai_codex_prompt'])){
            check_admin_referer('ai_codex_nonce');
            $prompt = sanitize_textarea_field($_POST['ai_codex_prompt']);
            $result = $this->call_openai($prompt);
            echo '<h2>生成结果</h2><pre style="white-space:pre-wrap;padding:10px;border:1px solid #ddd;">'.esc_html($result).'</pre>';
        }
        echo '<form method="post">';
        wp_nonce_field('ai_codex_nonce');
        echo '<textarea name="ai_codex_prompt" rows="8" cols="80" placeholder="在此输入提示（prompt）..."></textarea><br/><br/>';
        submit_button('生成');
        echo '</form></div>';
    }

    private function call_openai($prompt){
        $api_key = defined('OPENAI_API_KEY') ? OPENAI_API_KEY : get_option('ai_codex_api_key');
        if (!$api_key) return 'ERROR: OpenAI API key 未配置。请在 wp-config.php 定义 OPENAI_API_KEY 或在插件设置中保存。';

        $endpoint = 'https://api.openai.com/v1/chat/completions';
        $body = [
            'model' => 'gpt-4o-mini',
            'messages' => [
                ['role'=>'system','content'=>'你是 WordPress 内容助手。'],
                ['role'=>'user','content'=>$prompt]
            ],
            'max_tokens' => 600
        ];

        $args = [
            'headers' => [
                'Content-Type' => 'application/json',
                'Authorization' => 'Bearer ' . $api_key,
            ],
            'body' => wp_json_encode($body),
            'timeout' => 30,
        ];

        $resp = wp_remote_post($endpoint, $args);
        if (is_wp_error($resp)) return 'HTTP Error: ' . $resp->get_error_message();
        $code = wp_remote_retrieve_response_code($resp);
        $body = wp_remote_retrieve_body($resp);
        if ($code !== 200) return "API Error ({$code}): {$body}";
        $data = json_decode($body, true);
        return $data['choices'][0]['message']['content'] ?? json_encode($data);
    }

    public function register_routes(){
        register_rest_route('ai-codex/v1', '/generate', [
            'methods' => 'POST',
            'callback' => [$this, 'rest_generate'],
            'permission_callback' => function(){ return current_user_can('edit_posts'); }
        ]);
    }

    public function rest_generate($request){
        $prompt = sanitize_textarea_field($request->get_param('prompt'));
        $result = $this->call_openai($prompt);
        return rest_ensure_response(['result' => $result]);
    }
}

new AICodexAgent();
