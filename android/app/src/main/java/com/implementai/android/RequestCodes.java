package com.implementai.android;

import java.util.concurrent.atomic.AtomicInteger;

public class RequestCodes {
    // Need unique IDs for each request code to know discriminate between intents
    public static final AtomicInteger atomicInteger = new AtomicInteger();
    public static final int REQUEST_IMAGE_CAPTURE = atomicInteger.incrementAndGet();
    public static final int REQUEST_WRITE_STORAGE = atomicInteger.incrementAndGet();
    public static final int REQUEST_READ_STORAGE = atomicInteger.incrementAndGet();
    public static final int REQUEST_INTERNET = atomicInteger.incrementAndGet();
}
