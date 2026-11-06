# Stream Optimization Guide - Reducing Delay

## 🚀 **Optimizations Implemented**

### ✅ **Low-Latency Streaming**
- **Minimal buffer size** (1 frame) to reduce delay
- **Frame dropping** when behind to catch up
- **Aggressive timeout settings** for network streams
- **Resolution optimization** for better performance

### ✅ **Network Stream Optimizations**
- **RTSP**: TCP transport, H.264 codec, optimized resolution
- **HTTP/MJPEG**: MJPEG codec, reduced resolution for speed
- **USB Cameras**: Direct capture with minimal buffering

### ✅ **Performance Monitoring**
- **Real-time FPS tracking**
- **Latency measurement**
- **Buffer health indicators**
- **Performance warnings** when delay is high

## 🔧 **Settings to Reduce Delay**

### **Camera Settings**
1. **Enable "Low latency mode"** when adding cameras
2. **Set appropriate FPS** (30 FPS for most streams)
3. **Use lower resolution** if delay is critical
4. **Choose TCP transport** for RTSP streams

### **Network Optimization**
1. **Reduce connection timeout** (5-10 seconds)
2. **Lower reconnect interval** (2-5 seconds)
3. **Use wired connection** instead of WiFi when possible
4. **Ensure sufficient bandwidth** for all streams

### **System Performance**
1. **Close unnecessary applications**
2. **Use hardware acceleration** if available
3. **Reduce number of simultaneous streams** if needed
4. **Monitor CPU and memory usage**

## 📊 **Performance Indicators**

### **Good Performance**
- FPS matches target (±2 FPS)
- Latency < 100ms
- Buffer health: "Good"
- Smooth video playback

### **High Latency Warning**
- FPS significantly below target
- Latency 100-500ms
- Buffer health: "High"
- Occasional frame drops

### **Critical Performance**
- FPS much lower than target
- Latency > 500ms
- Buffer health: "Critical"
- Frequent buffering/freezing

## 🛠️ **Troubleshooting High Delay**

### **For RTSP Streams**
1. Check if camera supports TCP transport
2. Reduce stream resolution on camera
3. Lower bitrate settings on camera
4. Use direct IP connection (avoid DNS)

### **For HTTP/MJPEG Streams**
1. Reduce JPEG quality on camera
2. Lower frame rate on camera side
3. Check network congestion
4. Use dedicated network for cameras

### **For USB Cameras**
1. Use USB 3.0 ports
2. Reduce resolution/FPS in camera settings
3. Check USB cable quality
4. Avoid USB hubs when possible

## 📈 **Advanced Optimizations**

### **Camera-Side Settings**
- **I-frame interval**: Set to 1-2 seconds
- **Bitrate**: Match your network capacity
- **Resolution**: Use lowest acceptable quality
- **Codec**: H.264 for RTSP, MJPEG for HTTP

### **Network Configuration**
- **QoS**: Prioritize camera traffic
- **Multicast**: Use for multiple viewers
- **VLAN**: Separate camera network
- **Bandwidth**: 2-8 Mbps per HD stream

### **Application Settings**
- **Buffer size**: Keep at 1 for real-time
- **Thread priority**: Higher for stream threads
- **Memory**: Ensure sufficient RAM
- **Storage**: Fast SSD for recordings

## 🔍 **Monitoring Tools**

The application now shows:
- **Real-time FPS** in performance label
- **Latency measurements** in milliseconds
- **Buffer health status** (Good/High/Critical)
- **Connection status** in camera status bar

## 💡 **Best Practices**

1. **Test different settings** to find optimal configuration
2. **Monitor performance regularly** using built-in metrics
3. **Use consistent network conditions** for reliable streaming
4. **Keep camera firmware updated** for best performance
5. **Balance quality vs. latency** based on your needs

## 🚨 **Common Issues & Solutions**

| Issue | Cause | Solution |
|-------|-------|----------|
| High delay (>1 second) | Large buffer, network congestion | Enable low-latency mode, check network |
| Choppy video | Insufficient bandwidth | Reduce resolution/bitrate |
| Connection drops | Network instability | Increase timeout, use TCP |
| High CPU usage | Too many streams, high resolution | Reduce streams, lower quality |
| Memory leaks | Buffer accumulation | Restart streams periodically |

The optimized streaming system should significantly reduce delay compared to the original implementation!