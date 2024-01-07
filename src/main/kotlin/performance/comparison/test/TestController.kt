package performance.comparison.test

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController
import reactor.core.publisher.Mono
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL
import java.util.*


@RestController
class TestController {
    @GetMapping("standard")
    fun standard(): String {
        return base64()
    }

    @GetMapping("suspending")
    suspend fun suspending(): String {
        return base64()
    }

    @GetMapping("mono")
    fun mono(): Mono<String> {
        return Mono.fromRunnable { base64() }
    }


    private fun sleep(): String {
        Thread.sleep(1000)
        return "test"
    }

    private fun busyWait(): String {
        val startTime = System.currentTimeMillis()
        while (System.currentTimeMillis() - startTime < 1000) {
        }
        return "test"
    }

    private fun base64(): String {
        val string = generateTestString()

        val startTime = System.currentTimeMillis()
        while (System.currentTimeMillis() - startTime < 1000) {
            Base64.getEncoder().encode(string.toByteArray())
        }
        return "test"
    }

    private fun generateTestString(): String {
        val str = StringBuilder()
        for (i in 0 until 100000) {
            str.append(i % 255)
        }
        return str.toString()
    }


    fun httpRequest(): String {
        val url: URL = URL("http://localhost:8081/standard")
        val connection: HttpURLConnection = url.openConnection() as HttpURLConnection

        try {
            // Set request method to GET
            connection.setRequestMethod("GET")

            // Read the response
            val response = java.lang.StringBuilder()
            BufferedReader(InputStreamReader(connection.getInputStream())).use { reader ->
                var line: String?
                while ((reader.readLine().also { line = it }) != null) {
                    response.append(line)
                }
            }
            return response.toString()
        } finally {
            connection.disconnect()
        }
    }
}
