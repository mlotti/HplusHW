double pileupWeightEPS(double npu) {
  static double weights[] = {
    0.127326,
    0.450547,
    1.03008,
    1.65103,
    2.08362,
    2.18915,
    1.99759,
    1.62489,
    1.21858,
    0.859666,
    0.586923,
    0.391112,
    0.2603,
    0.171094,
    0.113608,
    0.075273,
    0.050617,
    0.0338315,
    0.022959,
    0.0158491,
    0.0107926,
    0.00746603,
    0.00509296,
    0.00358601,
    0.00372379
  };
  size_t n = sizeof(weights)/sizeof(double);

  int index = int(npu);
  if(index < 0)
    index = 0;
  if(index >= n)
    index = n-1;

  return weights[index];
}
