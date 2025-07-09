Texture2D src : register(t0);

cbuffer constant0 : register(b0) {
    float3 normal;
    float3x3 mat1;
    float3x3 mat2;
    float severity;
};

float3 SRGBToLinear(float3 srgb) {
    float3 low  = srgb / 12.92;
    float3 high = pow(abs((srgb + 0.055) / 1.055), 2.4);
    float3 mask = step(0.04045, srgb);
    return lerp(low, high, mask);
}

float3 LinearToSRGB(float3 lrgb) {
    float3 low  = lrgb * 12.92;
    float3 high = 1.055 * pow(abs(lrgb), 1.0 / 2.4) - 0.055;
    float3 mask = step(0.0031308, lrgb);
    return lerp(low, high, mask);
}

float4 brettel1997(float4 pos : SV_Position) : SV_Target {
    float4 color = src.Load(int3(pos.xy, 0));
    float3 linearColor = SRGBToLinear(color.rgb);
    float x = dot(linearColor, normal);
    float3 high = mul(linearColor, mat1);
    float3 low = mul(linearColor, mat2);
    float3 simColor = lerp(low, high, step(0.0, x));
    float3 resultColor = lerp(linearColor, simColor, severity);
    return float4(LinearToSRGB(resultColor), color.a);
}
