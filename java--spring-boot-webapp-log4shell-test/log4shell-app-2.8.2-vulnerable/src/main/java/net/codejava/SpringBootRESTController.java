package net.codejava;
 
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestHeader;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
 
@RestController
public class SpringBootRESTController {

    private static final Logger logger = LogManager.getLogger("SpringBootHelloWorld");

    @RequestMapping("/")
    String home(@RequestHeader(value = "User-Agent") String userAgent) {
        logger.info("Got request from user agent: {}", userAgent);
        return "Hello World Spring Boot!";
    }

}
