# JMeter Test Plan Template Reference

This document provides the XML skeleton for generating `.jmx` JMeter test plans programmatically. Agents should use this as a structural reference when creating new test plans for different workflows or endpoints.

## XML Structure Overview

A JMeter `.jmx` file follows this hierarchy:

```
TestPlan
└── ThreadGroup
    ├── CSV Data Set Config(s)
    ├── HTTP Request Defaults
    ├── HTTP Header Manager
    ├── Cookie Manager (optional)
    ├── Sampler 1: HTTP Request
    │   ├── JSON Extractor (optional)
    │   └── Response Assertion
    ├── Sampler 2: HTTP Request
    │   └── Response Assertion
    ├── ... more samplers ...
    ├── Timer (Gaussian Random Timer)
    └── Listener (Aggregate / Summary / View Results Tree)
```

## ThreadGroup Configuration Patterns

### Load Test
```xml
<ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup">
  <intProp name="ThreadGroup.num_threads">10</intProp>
  <intProp name="ThreadGroup.ramp_time">10</intProp>
  <elementProp name="ThreadGroup.main_controller">
    <intProp name="LoopController.loops">5</intProp>
  </elementProp>
</ThreadGroup>
```

### Stress Test
```xml
<ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup">
  <intProp name="ThreadGroup.num_threads">50</intProp>
  <intProp name="ThreadGroup.ramp_time">15</intProp>
  <elementProp name="ThreadGroup.main_controller">
    <intProp name="LoopController.loops">10</intProp>
  </elementProp>
</ThreadGroup>
```

### Spike Test
```xml
<ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup">
  <intProp name="ThreadGroup.num_threads">100</intProp>
  <intProp name="ThreadGroup.ramp_time">1</intProp>
  <elementProp name="ThreadGroup.main_controller">
    <intProp name="LoopController.loops">3</intProp>
  </elementProp>
</ThreadGroup>
```

## Key Component Templates

### CSV Data Set Config
```xml
<CSVDataSet guiclass="TestBeanGUI" testclass="CSVDataSet">
  <stringProp name="filename">data/credentials.csv</stringProp>
  <stringProp name="delimiter">,</stringProp>
  <stringProp name="variableNames">email,password</stringProp>
  <boolProp name="recycle">true</boolProp>
  <stringProp name="shareMode">shareMode.all</stringProp>
</CSVDataSet>
```

### HTTP Request Defaults
```xml
<ConfigTestElement guiclass="HttpDefaultsGui" testclass="ConfigTestElement">
  <stringProp name="HTTPSampler.domain">localhost</stringProp>
  <intProp name="HTTPSampler.port">3000</intProp>
  <stringProp name="HTTPSampler.protocol">http</stringProp>
</ConfigTestElement>
```

### JSON Extractor (for JWT tokens, created IDs)
```xml
<JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor">
  <stringProp name="JSONPostProcessor.referenceNames">auth_token</stringProp>
  <stringProp name="JSONPostProcessor.jsonPathExprs">$.token</stringProp>
  <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
</JSONPostProcessor>
```

### Response Assertion
```xml
<ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion">
  <collectionProp name="Asserion.test_strings">
    <stringProp>200</stringProp>
  </collectionProp>
  <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
  <intProp name="Assertion.test_type">8</intProp>
</ResponseAssertion>
```

### Gaussian Random Timer
```xml
<!-- Load: mean 2000ms, sigma 333ms; about 99.7% falls within 1000-3000ms. -->
<GaussianRandomTimer guiclass="GaussianRandomTimerGui" testclass="GaussianRandomTimer">
  <stringProp name="ConstantTimer.delay">2000</stringProp>
  <stringProp name="RandomTimer.range">333</stringProp>
</GaussianRandomTimer>

<!-- Stress: mean 1000ms, sigma 167ms; about 99.7% falls within 500-1500ms. -->
<GaussianRandomTimer guiclass="GaussianRandomTimerGui" testclass="GaussianRandomTimer">
  <stringProp name="ConstantTimer.delay">1000</stringProp>
  <stringProp name="RandomTimer.range">167</stringProp>
</GaussianRandomTimer>

<!-- Spike: No timer (omit entirely) -->
```

`ConstantTimer.delay` is the distribution mean/offset and `RandomTimer.range`
is the standard deviation. A Gaussian distribution is unbounded, so these are
target ranges, not hard minimum and maximum delays.

### Listener Types (use one per plan, all different)

**Aggregate Report:**
```xml
<ResultCollector guiclass="StatVisualizer" testclass="ResultCollector">
  <stringProp name="filename">results/load/raw.jtl</stringProp>
</ResultCollector>
```

**Summary Report:**
```xml
<ResultCollector guiclass="SummaryReport" testclass="ResultCollector">
  <stringProp name="filename">results/stress/raw.jtl</stringProp>
</ResultCollector>
```

**View Results Tree:**
```xml
<ResultCollector guiclass="ViewResultsFullVisualizer" testclass="ResultCollector">
  <stringProp name="filename">results/spike/raw.jtl</stringProp>
  <boolProp name="ResultCollector.error_logging">false</boolProp>
</ResultCollector>
```

## HTTP Request Sampler with Auth Header

```xml
<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy">
  <stringProp name="HTTPSampler.path">/api/admin/users</stringProp>
  <stringProp name="HTTPSampler.method">GET</stringProp>
  <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
  <elementProp name="HTTPsampler.Arguments">
    <!-- empty for GET -->
  </elementProp>
</HTTPSamplerProxy>
<!-- Pair with Header Manager containing: Authorization = Bearer ${auth_token} -->
```

## POST Request with JSON Body

```xml
<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy">
  <stringProp name="HTTPSampler.path">/api/products</stringProp>
  <stringProp name="HTTPSampler.method">POST</stringProp>
  <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
  <elementProp name="HTTPsampler.Arguments">
    <collectionProp>
      <elementProp>
        <stringProp name="Argument.value">{"name":"${product_name}","price":${price},"description":"${description}","imageUrl":"${imageUrl}","category_id":${category_id}}</stringProp>
      </elementProp>
    </collectionProp>
  </elementProp>
</HTTPSamplerProxy>
```
