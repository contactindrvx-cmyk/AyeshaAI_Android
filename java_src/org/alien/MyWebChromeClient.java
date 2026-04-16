package org.alien;

import android.webkit.WebChromeClient;
import android.webkit.PermissionRequest;

public class MyWebChromeClient extends WebChromeClient {
    @Override
    public void onPermissionRequest(final PermissionRequest request) {
        // یہ جادوئی لائن WebView کی تمام پرمیشنز کو خاموشی سے الاؤ کر دے گی
        request.grant(request.getResources());
    }
}
