package performance.comparison.test

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController
import reactor.core.publisher.Mono
import java.util.Base64

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
}
