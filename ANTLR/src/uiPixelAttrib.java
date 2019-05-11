public class uiPixelAttrib {
    double r, g, b, s;
    uiPixelAttrib(double _r, double _g, double _b) {
        r = _r; g = _g; b = _b; s = 10;
    }
    uiPixelAttrib() {
        r = g = b = 0;
        s = 10;
    }
    double red() { return r;}
    double green() { return g;}
    double blue() { return b;}
    double size() { return s;}
}