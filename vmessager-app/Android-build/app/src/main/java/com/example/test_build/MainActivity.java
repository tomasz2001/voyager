package com.example.test_build;

import android.os.Bundle;
import android.os.Handler;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private boolean visible = true; // czy tekst jest widoczny
    private Handler handler = new Handler(); // obsługuje powtarzanie co jakiś czas

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.text);

        // Zadanie, które zmienia tekst co 0.5 sekundy
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                if (visible) {
                    textView.setText("every body is mlem"); // ukryj
                } else {
                    textView.setText("Hello World!"); // pokaż
                }
                visible = !visible;

                // ponownie uruchom po 500 ms
                handler.postDelayed(this, 500);
            }
        };

        // uruchom pierwszy raz
        handler.post(runnable);
    }
}
