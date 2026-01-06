package com.example.icptest

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.TextView
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody

class MainActivity : AppCompatActivity() {

    private val client = OkHttpClient()
    private lateinit var responseText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        responseText = findViewById(R.id.icpResponse)

        // start testu ICP
        testIcpQuery()
    }

    private fun testIcpQuery() {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val canisterId = "ryjl3-tyaaa-aaaaa-aaaba-cai" // <- swój wstaw
                val url = "https://ic0.app/api/v2/canister/$canisterId/query"

                val jsonBody = """
                    {
                      "request_type": "query",
                      "canister_id": "$canisterId",
                      "method_name": "greet",
                      "arg": ""
                    }
                """.trimIndent()

                val body = jsonBody.toRequestBody("application/json".toMediaType())

                val request = Request.Builder()
                    .url(url)
                    .post(body)
                    .build()

                val response = client.newCall(request).execute()
                val responseTextRaw = response.body?.string() ?: "Brak odpowiedzi"

                Log.d("ICP_TEST", "Response: $responseTextRaw")

                // wyświetlenie na ekranie
                withContext(Dispatchers.Main) {
                    responseText.text = responseTextRaw
                }

            } catch (e: Exception) {
                Log.e("ICP_TEST", "Error: ${e.message}", e)
                withContext(Dispatchers.Main) {
                    responseText.text = "Błąd: ${e.message}"
                }
            }
        }
    }
}