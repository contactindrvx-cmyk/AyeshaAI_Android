package com.raza.alien;

import android.webkit.WebChromeClient;
import android.webkit.PermissionRequest;

public class MyWebClient extends WebChromeClient {
    @Override
    public void onPermissionRequest(final PermissionRequest request) {
        request.grant(request.getResources());
    }
}
