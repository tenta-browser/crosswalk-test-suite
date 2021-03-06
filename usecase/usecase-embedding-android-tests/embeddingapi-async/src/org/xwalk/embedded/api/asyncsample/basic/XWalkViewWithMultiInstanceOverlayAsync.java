// Copyright (c) 2014 Intel Corporation. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

package org.xwalk.embedded.api.asyncsample.basic;

import org.xwalk.embedded.api.asyncsample.R;

import android.app.Activity;
import org.xwalk.core.XWalkInitializer;
import org.xwalk.core.XWalkView;

import android.app.AlertDialog;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.TextView;

public class XWalkViewWithMultiInstanceOverlayAsync extends Activity implements XWalkInitializer.XWalkInitListener {
    private XWalkView mXWalkView;
    private XWalkView mXWalkView2;
    private Button mSwapButton;
    private TextView mOverlayLabel;
    private XWalkInitializer mXWalkInitializer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        mXWalkInitializer = new XWalkInitializer(this, this);
        mXWalkInitializer.initAsync();
    }

    @Override
    public final void onXWalkInitStarted() {
        // It's okay to do nothing
    }

    @Override
    public final void onXWalkInitCancelled() {
        // It's okay to do nothing
    }

    @Override
    public final void onXWalkInitFailed() {
        // Do crash or logging or anything else in order to let the tester know if this method get called
    }

    @Override
    public final void onXWalkInitCompleted() {
        StringBuffer mess = new StringBuffer();
        mess.append("Test Purpose: \n\n")
        .append("Verifies two xwalkviews filling in the same parent view can be displayed dynamically.\n\n")
        .append("Expected Result:\n\n")
        .append("Test passes if app load 'sogou' and 'baidu' dynamically by swap button.");
        new  AlertDialog.Builder(this)
        .setTitle("Info" )
        .setMessage(mess.toString())
        .setPositiveButton("confirm" ,  null)
        .show();

        setContentView(R.layout.activity_xwalk_view_with_multi_instance_overlay);

        FrameLayout parent = (FrameLayout) findViewById(R.id.overlay_container);

        FrameLayout.LayoutParams params = new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT);

        mOverlayLabel = (TextView) findViewById(R.id.xwalk_overlay_label);
        mSwapButton = (Button) findViewById(R.id.swap_button);
        mSwapButton.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View v) {
                // TODO Auto-generated method stub
                if (mXWalkView.getVisibility() == View.VISIBLE) {
                    mXWalkView.setVisibility(View.INVISIBLE);
                    mXWalkView2.setVisibility(View.VISIBLE);
                    mOverlayLabel.setText("sogou visibility: INVISIBLE; baidu visibility: VISIBLE");
                } else {
                    mXWalkView.setVisibility(View.VISIBLE);
                    mXWalkView2.setVisibility(View.INVISIBLE);
                    mOverlayLabel.setText("sogou visibility: VISIBLE; baidu visibility: INVISIBLE");
                }
            }
        });

        mXWalkView = new XWalkView(this, this);
        parent.addView(mXWalkView, params);
        mXWalkView.setVisibility(View.VISIBLE);

        mXWalkView2 = new XWalkView(this, this);
        parent.addView(mXWalkView2, params);
        mXWalkView2.setVisibility(View.INVISIBLE);

        mXWalkView.load("http://www.sogou.com", null);
        mXWalkView2.load("http://www.baidu.com", null);

        mOverlayLabel.setText("sogou visibility: VISIBLE; baidu visibility: INVISIBLE");
    }

}
