package com.example.bokyeong.bblur;

import android.content.Intent;
import android.database.Cursor;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    private static int PICK_IMAGE_REQUEST = 1;
    private static int PICK_VIDEO_REQUEST = 2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

    }

    // 갤러리에서 이미지 선택
    public void selectPhotofromGallery(View view) {

        startActivityForResult(
            Intent.createChooser(
                new Intent(Intent.ACTION_GET_CONTENT)
                        .setType("image/*"), "Select Picture"), PICK_IMAGE_REQUEST);
    }

    // 갤러리에서 동영상 선택
    public void selectVideofromGallery(View view) {

        startActivityForResult(
                Intent.createChooser(
                        new Intent(Intent.ACTION_GET_CONTENT)
                                .setType("video/*"), "Select Video"), PICK_VIDEO_REQUEST);
    }


    // image path 얻기
    public String getPath(Uri uri) {

        if( uri == null ) {
            return null;
        }

        // this will only work for images selected from gallery
        String[] projection = { MediaStore.Images.Media.DATA };
        Cursor cursor = managedQuery(uri, projection, null, null, null);
        if( cursor != null ){
            int column_index = cursor
                    .getColumnIndexOrThrow(MediaStore.Images.Media.DATA);
            cursor.moveToFirst();
            return cursor.getString(column_index);
        }

        return uri.getPath();
    }

    // 데이터 파일 선택 후의 결과 처리
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        try {
            //이미지를 선택한 경우
            if (requestCode == PICK_IMAGE_REQUEST && resultCode == RESULT_OK && null != data) {

                Uri uri = (Uri)data.getData();

                String selectedImagePath = getPath(uri);

                Intent intent = new Intent(MainActivity.this, SendToServer.class);
                intent.putExtra("imageUri", uri);
                intent.putExtra("imagePath", selectedImagePath);


                startActivity(intent);

            }
            //비디오를 선택한 경우
            else if (requestCode == PICK_VIDEO_REQUEST && resultCode == RESULT_OK && null != data)
            {
                Uri uri = (Uri)data.getData();

                Intent intent = new Intent(MainActivity.this, VideoActivity.class);
                intent.putExtra("videoUri", uri);

                startActivity(intent);
            }
        }catch (Exception e) {
            Toast.makeText(this, "오류가 발생했습니다.", Toast.LENGTH_LONG).show();
            e.printStackTrace();
        }
    }
}
