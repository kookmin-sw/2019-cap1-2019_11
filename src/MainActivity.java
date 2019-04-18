package com.example.bokyeong.bblur;

import android.content.Intent;
import android.database.Cursor;
import android.database.DatabaseUtils;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.media.MediaMetadataRetriever;
import android.net.Uri;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;
import android.widget.VideoView;

import java.io.InputStream;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    private static int PICK_IMAGE_REQUEST = 1;
    private static int PICK_VIDEO_REQUEST = 2;

    ImageView imgView;
    VideoView videoView;

    static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    // 갤러리에서 이미지 선택
    public void loadImagefromGallery(View view) {

        startActivityForResult(
                Intent.createChooser(
                        new Intent(Intent.ACTION_GET_CONTENT)
                                .setType("image/*"), "Select Picture"),
                PICK_IMAGE_REQUEST);

    }

    // 갤러리에서 동영상 선택
    public void loadVideofromGallery(View view) {

        startActivityForResult(
                Intent.createChooser(
                        new Intent(Intent.ACTION_GET_CONTENT)
                                .setType("video/*"), "Select Video"),
                PICK_VIDEO_REQUEST);

    }

    // 데이터 파일 선택 후의 결과 처리
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        try {
            //이미지를 선택한 경우
            if (requestCode == PICK_IMAGE_REQUEST && resultCode == RESULT_OK && null != data) {

                Uri uri = data.getData();
                Log.d("data", data.toString());

                Bitmap bitmap = null;
                bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), uri);

                int nh = (int) (bitmap.getHeight() * (1024.0 / bitmap.getWidth()));
                Bitmap scaled = Bitmap.createScaledBitmap(bitmap, 1024, nh, true);

                imgView = (ImageView) findViewById(R.id.imageView);
                imgView.setImageBitmap(scaled);
            }

            //비디오를 선택한 경우
            else if (requestCode == PICK_VIDEO_REQUEST && resultCode == RESULT_OK && null != data)
            {
                Uri uri = data.getData();

                videoView = (VideoView) findViewById(R.id.videoView);

                videoView.setVideoURI(Uri.parse(String.valueOf(uri)));
                videoView.requestFocus();

                videoView.start();
            }
            else {
                Toast.makeText(this, "취소 되었습니다.", Toast.LENGTH_LONG).show();
            }

        } catch (Exception e) {
            Toast.makeText(this, "오류가 발생했습니다.", Toast.LENGTH_LONG).show();
            e.printStackTrace();
        }

    }
}
