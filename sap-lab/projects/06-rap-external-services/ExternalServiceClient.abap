*&---------------------------------------------------------------------*
*& HTTP Client Service 示例
*&---------------------------------------------------------------------*

CLASS lcl_http_client_service DEFINITION.

  PUBLIC SECTION.

    TYPES: BEGIN OF ts_response,
             status_code TYPE i,
             status_text TYPE string,
             body        TYPE string,
           END OF ts_response.

    METHODS call_external_api
      IMPORTING
        iv_url      TYPE string
        iv_method   TYPE string DEFAULT 'GET'
        iv_body     TYPE string OPTIONAL
      RETURNING
        VALUE(rs_response) TYPE ts_response
      RAISING
        cx_http_dest_provider_error
        cx_web_http_client_error.

  PRIVATE SECTION.

    DATA mv_destination TYPE string VALUE 'EXTERNAL_SERVICE'.

ENDCLASS.

CLASS lcl_http_client_service IMPLEMENTATION.

  METHOD call_external_api.

    TRY.
        " 获取 HTTP 目标
        DATA(lo_http_client) = cl_web_http_client_manager=>create_by_http_destination(
          cl_http_destination_provider=>create_by_url( iv_url )
        ).

        " 构建请求
        DATA(lo_request) = lo_http_client->get_http_request( ).
        lo_request->set_header_field( i_name = 'Content-Type' i_value = 'application/json' ).

        IF iv_method = 'POST' OR iv_method = 'PUT'.
          lo_request->set_text( iv_body ).
        ENDIF.

        " 执行请求
        DATA(lo_response) = lo_http_client->execute(
          i_method = iv_method
        ).

        " 处理响应
        rs_response-status_code = lo_response->get_status( )-code.
        rs_response-status_text = lo_response->get_status( )-reason.
        rs_response-body = lo_response->get_text( ).

        IF rs_response-status_code >= 400.
          " 错误处理
          RAISE EXCEPTION TYPE cx_web_http_client_error
            EXPORTING
              previous = NEW cx_web_http_client_error(
                textid = cx_web_http_client_error=>request_error
              ).
        ENDIF.

      CATCH cx_http_dest_provider_error INTO DATA(lo_ex).
        WRITE: / 'Destination Error:', lo_ex->get_text( ).
        RAISE.
      CATCH cx_web_http_client_error INTO DATA(lo_ex2).
        WRITE: / 'HTTP Client Error:', lo_ex2->get_text( ).
        RAISE.

    ENDTRY.

  ENDMETHOD.

ENDCLASS.


*&---------------------------------------------------------------------*
*& 使用示例
*&---------------------------------------------------------------------*

PROGRAM zexample_external_service.

START-OF-SELECTION.

  DATA(lo_service) = NEW lcl_http_client_service( ).

  " 调用天气 API
  TRY.
      DATA(ls_response) = lo_service->call_external_api(
        iv_url = 'https://api.example.com/weather?city=Beijing'
        iv_method = 'GET'
      ).

      WRITE: / 'Status Code:', ls_response-status_code.
      WRITE: / 'Response Body:', ls_response-body.

    CATCH cx_web_http_client_error INTO DATA(lo_ex).
      WRITE: / 'Error:', lo_ex->get_text( ).
  ENDTRY.
