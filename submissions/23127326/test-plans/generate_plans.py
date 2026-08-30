#!/usr/bin/env python3
"""Generate the three reviewed JMeter plans from one shared workflow."""

from pathlib import Path
import os
from xml.etree import ElementTree as ET

OUT = Path(__file__).parent
RUN_DATE = os.environ.get("RUN_DATE", "YYYYMMDD")
STUDENT_ID = os.environ.get("STUDENT_ID", "23127326")


def make(tag, attrs=None):
    return ET.Element(tag, attrs or {})


def child(parent, tag, attrs=None, text=None):
    item = ET.SubElement(parent, tag, attrs or {})
    if text is not None:
        item.text = text
    return item


def prop(parent, tag, name, value=""):
    child(parent, tag, {"name": name}, value)


def pair(parent_hash, element, children=()):
    parent_hash.append(element)
    element_hash = child(parent_hash, "hashTree")
    for item, nested in children:
        pair(element_hash, item, nested)


def groovy(*lines):
    return "\n".join(lines)


def bean(tag, name, testclass, properties, guiclass="TestBeanGUI"):
    element = make(tag, {"guiclass": guiclass, "testclass": testclass, "testname": name, "enabled": "true"})
    for kind, key, value in properties:
        prop(element, kind, key, value)
    return element


def sampler(name, method, path, body=None, args=()):
    element = make("HTTPSamplerProxy", {"guiclass": "HttpTestSampleGui", "testclass": "HTTPSamplerProxy", "testname": name, "enabled": "true"})
    common = [("stringProp", "HTTPSampler.domain", "${baseHost}"), ("stringProp", "HTTPSampler.port", "${basePort}"), ("stringProp", "HTTPSampler.protocol", "${baseProtocol}"), ("stringProp", "HTTPSampler.path", path), ("stringProp", "HTTPSampler.method", method), ("boolProp", "HTTPSampler.follow_redirects", "true"), ("boolProp", "HTTPSampler.auto_redirects", "false"), ("boolProp", "HTTPSampler.use_keepalive", "true"), ("boolProp", "HTTPSampler.DO_MULTIPART_POST", "false"), ("stringProp", "HTTPSampler.embedded_url_re", ""), ("stringProp", "HTTPSampler.connect_timeout", ""), ("stringProp", "HTTPSampler.response_timeout", "")]
    for kind, key, value in common:
        prop(element, kind, key, value)
    prop(element, "boolProp", "HTTPSampler.postBodyRaw", "true" if body is not None else "false")
    arguments = child(element, "elementProp", {"name": "HTTPsampler.Arguments", "elementType": "Arguments", "guiclass": "HTTPArgumentsPanel", "testclass": "Arguments", "testname": "User Defined Variables", "enabled": "true"})
    collection = child(arguments, "collectionProp", {"name": "Arguments.arguments"})
    if body is not None:
        item = child(collection, "elementProp", {"name": "", "elementType": "HTTPArgument"})
        prop(item, "boolProp", "HTTPArgument.always_encode", "false")
        prop(item, "stringProp", "Argument.value", body)
        prop(item, "stringProp", "Argument.metadata", "=")
        prop(item, "boolProp", "HTTPArgument.use_equals", "false")
    else:
        for arg_name, arg_value in args:
            item = child(collection, "elementProp", {"name": "", "elementType": "HTTPArgument"})
            prop(item, "boolProp", "HTTPArgument.always_encode", "true")
            prop(item, "stringProp", "Argument.name", arg_name)
            prop(item, "stringProp", "Argument.value", arg_value)
            prop(item, "boolProp", "HTTPArgument.use_equals", "true")
            prop(item, "stringProp", "Argument.metadata", "=")
    prop(element, "stringProp", "HTTPSampler.implementation", "HttpClient4")
    return element


def status_assertion(code):
    element = make("ResponseAssertion", {"guiclass": "AssertionGui", "testclass": "ResponseAssertion", "testname": f"HTTP status is {code}", "enabled": "true"})
    values = child(element, "collectionProp", {"name": "Asserion.test_strings"})
    child(values, "stringProp", {"name": ""}, str(code))
    prop(element, "stringProp", "Assertion.test_field", "Assertion.response_code")
    prop(element, "intProp", "Assertion.test_type", "8")
    prop(element, "stringProp", "Assertion.custom_message", "")
    prop(element, "boolProp", "Assertion.assume_success", "false")
    return element


def extract(name, path):
    return bean("JSONPostProcessor", name, "JSONPostProcessor", [("stringProp", "JSONPostProcessor.referenceNames", name), ("stringProp", "JSONPostProcessor.jsonPathExprs", path), ("stringProp", "JSONPostProcessor.match_numbers", "1"), ("stringProp", "JSONPostProcessor.defaultValues", "NOT_FOUND")], guiclass="JSONPostProcessorGui")


def jsr_sampler(name, script):
    return bean("JSR223Sampler", name, "JSR223Sampler", [("stringProp", "scriptLanguage", "groovy"), ("stringProp", "parameters", ""), ("stringProp", "filename", ""), ("stringProp", "cacheKey", "true"), ("stringProp", "script", script)])


def jsr_assertion(name, script):
    return bean("JSR223Assertion", name, "JSR223Assertion", [("stringProp", "scriptLanguage", "groovy"), ("stringProp", "parameters", ""), ("stringProp", "filename", ""), ("stringProp", "cacheKey", "true"), ("stringProp", "script", script)])


def jsr_postprocessor(name, script):
    return bean("JSR223PostProcessor", name, "JSR223PostProcessor", [("stringProp", "scriptLanguage", "groovy"), ("stringProp", "parameters", ""), ("stringProp", "filename", ""), ("stringProp", "cacheKey", "true"), ("stringProp", "script", script)])


def csv(name, variables):
    return bean("CSVDataSet", f"CSV - {name}", "CSVDataSet", [("stringProp", "filename", f"${{dataDir}}/{name}"), ("stringProp", "fileEncoding", "UTF-8"), ("stringProp", "variableNames", variables), ("boolProp", "ignoreFirstLine", "true"), ("boolProp", "quotedData", "true"), ("boolProp", "recycle", "false"), ("boolProp", "stopThread", "true"), ("stringProp", "shareMode", "shareMode.all")])


def header_manager():
    element = make("HeaderManager", {"guiclass": "HeaderPanel", "testclass": "HeaderManager", "testname": "JSON and Bearer headers", "enabled": "true"})
    collection = child(element, "collectionProp", {"name": "HeaderManager.headers"})
    for name, value in (("Content-Type", "application/json"), ("Authorization", "Bearer ${token}")):
        item = child(collection, "elementProp", {"name": "", "elementType": "Header"})
        prop(item, "stringProp", "Header.name", name)
        prop(item, "stringProp", "Header.value", value)
    return element


def timer():
    return bean("UniformRandomTimer", "Think time 1-3 seconds", "UniformRandomTimer", [("stringProp", "ConstantTimer.delay", "${thinkMinMs}"), ("stringProp", "RandomTimer.range", "${thinkMaxMs}")], guiclass="UniformRandomTimerGui")


def setup_url():
    return jsr_sampler("SETUP_BASE_URL", groovy(
        "def value = vars.get('baseUrl')",
        r"def matcher = (value =~ /^(https?):\/\/([^:\/]+)(?::(\d+))?/)",
        "if (!matcher.find()) { throw new IllegalArgumentException('Invalid baseUrl: ' + value) }",
        "vars.put('baseProtocol', matcher.group(1))",
        "vars.put('baseHost', matcher.group(2))",
        "vars.put('basePort', matcher.group(3) ?: (matcher.group(1) == 'https' ? '443' : '80'))",
    ))


def workflow():
    login = sampler("AUTH - login", "POST", "/api/login", '{"email":"${email}","password":"${password}"}')
    login_kids = [(extract("token", "$.token"), ()), (status_assertion(200), ()), (jsr_assertion("Login response has token", groovy("if (!vars.get('token') || vars.get('token') == 'NOT_FOUND') { AssertionResult.setFailure(true); AssertionResult.setFailureMessage('Missing token') }")), ())]

    products = sampler("READ - search products", "GET", "/api/products", args=(("search", "${search}"), ("page", "${page}"), ("limit", "${limit}")))
    product_check = groovy(
        "def body = new groovy.json.JsonSlurper().parseText(prev.getResponseDataAsString())",
        "def key = vars.get('search').toLowerCase()",
        "if (!(body instanceof List) || body.isEmpty()) { AssertionResult.setFailure(true); AssertionResult.setFailureMessage('Product list is empty') }",
        "else if (!body.any { (it.name ?: '').toString().toLowerCase().contains(key) }) { AssertionResult.setFailure(true); AssertionResult.setFailureMessage('No product matches search') }",
    )
    product_kids = [(status_assertion(200), ()), (extract("productId", "$[0].id"), ()), (extract("productName", "$[0].name"), ()), (extract("productPrice", "$[0].price"), ()), (jsr_assertion("Product response is non-empty and matches search", product_check), ())]

    cart_add = sampler("CART_ADD - initial quantity", "POST", "/api/cart", '{"id":${productId},"name":"${productName}","price":${productPrice},"quantity":${quantity_initial}}')
    cart_update = sampler("CART_UPDATE - requested quantity", "POST", "/api/cart", '{"id":${productId},"name":"${productName}","price":${productPrice},"quantity":${quantity_updated}}')
    cart = sampler("CART_GET - verify update", "GET", "/api/cart")
    cart_check = groovy(
        "def cart = new groovy.json.JsonSlurper().parseText(prev.getResponseDataAsString())",
        "def rows = cart.findAll { it.id.toString() == vars.get('productId') }",
        "def quantities = rows.collect { (it.quantity as BigDecimal).intValue() }",
        "def expected = (vars.get('quantity_updated') as BigDecimal).intValue()",
        "def compliant = rows.size() == 1 && quantities[0] == expected",
        "vars.put('cartUpdateCompliant', compliant.toString())",
        "if (!compliant) { log.warn('BUSINESS_GAP cart update: expected one row at quantity ' + expected + ', actual rows=' + rows.size() + ', quantities=' + quantities) }",
    )
    cart_kids = [(status_assertion(200), ()), (jsr_postprocessor("Capture cart update business result", cart_check), ())]

    total = jsr_sampler("CALCULATE_ORDER_TOTAL", groovy("def total = (vars.get('productPrice') as BigDecimal) * (vars.get('quantity_updated') as BigDecimal)", "vars.put('orderTotal', total.toBigInteger().toString())"))
    checkout = sampler("CHECKOUT - create order", "POST", "/api/checkout", '{"total_amount":${orderTotal},"shipping_address":"${shipping_address}"}')
    checkout_kids = [(status_assertion(200), ()), (extract("orderId", "$.orderId"), ()), (jsr_assertion("Checkout response has orderId", groovy("if (!vars.get('orderId') || vars.get('orderId') == 'NOT_FOUND') { AssertionResult.setFailure(true); AssertionResult.setFailureMessage('Missing orderId') }")), ())]

    post_cart = sampler("POST_CHECKOUT_CART - expected empty", "GET", "/api/cart")
    post_check = groovy("def cart = new groovy.json.JsonSlurper().parseText(prev.getResponseDataAsString())", "if (!(cart instanceof List) || !cart.isEmpty()) { AssertionResult.setFailure(true); AssertionResult.setFailureMessage('Known business gap: cart not empty after checkout') }")
    post_kids = [(status_assertion(200), ()), (jsr_assertion("Cart is empty after checkout", post_check), ())]
    return [(setup_url(), ()), (login, login_kids), (products, product_kids), (cart_add, [(status_assertion(200), ())]), (cart_update, [(status_assertion(200), ())]), (cart, cart_kids), (total, ()), (checkout, checkout_kids), (post_cart, post_kids)]


def group(name, threads, ramp, duration, delay="0", input_file="per-vu/input-${__threadNum}.csv"):
    element = make("ThreadGroup", {"guiclass": "ThreadGroupGui", "testclass": "ThreadGroup", "testname": name, "enabled": "true"})
    prop(element, "stringProp", "ThreadGroup.on_sample_error", "continue")
    controller = child(element, "elementProp", {"name": "ThreadGroup.main_controller", "elementType": "LoopController", "guiclass": "LoopControlPanel", "testclass": "LoopController", "enabled": "true"})
    prop(controller, "boolProp", "LoopController.continue_forever", "true")
    prop(controller, "stringProp", "LoopController.loops", "-1")
    for kind, key, value in (("stringProp", "ThreadGroup.num_threads", threads), ("stringProp", "ThreadGroup.ramp_time", ramp), ("longProp", "ThreadGroup.start_time", "0"), ("longProp", "ThreadGroup.end_time", "0"), ("boolProp", "ThreadGroup.scheduler", "true"), ("stringProp", "ThreadGroup.duration", duration), ("stringProp", "ThreadGroup.delay", delay)):
        prop(element, kind, key, value)
    input_values = [(csv(input_file, "email,password,search,page,limit,product_id,product_name,price,quantity_initial,quantity_updated,shipping_address"), ())]
    workflow_controller = make("GenericController", {"guiclass": "LogicControllerGui", "testclass": "GenericController", "testname": "E2E workflow", "enabled": "true"})
    return element, input_values + [(header_manager(), ()), (timer(), ()), (workflow_controller, workflow())]


def lockout_group():
    element = make("ThreadGroup", {"guiclass": "ThreadGroupGui", "testclass": "ThreadGroup", "testname": "LOCKOUT_PROBE - disabled for official run", "enabled": "false"})
    prop(element, "stringProp", "ThreadGroup.on_sample_error", "continue")
    controller = child(element, "elementProp", {"name": "ThreadGroup.main_controller", "elementType": "LoopController", "guiclass": "LoopControlPanel", "testclass": "LoopController", "enabled": "true"})
    prop(controller, "boolProp", "LoopController.continue_forever", "false")
    prop(controller, "stringProp", "LoopController.loops", "1")
    for kind, key, value in (("stringProp", "ThreadGroup.num_threads", "1"), ("stringProp", "ThreadGroup.ramp_time", "1"), ("longProp", "ThreadGroup.start_time", "0"), ("longProp", "ThreadGroup.end_time", "0"), ("boolProp", "ThreadGroup.scheduler", "false"), ("stringProp", "ThreadGroup.duration", ""), ("stringProp", "ThreadGroup.delay", "")):
        prop(element, kind, key, value)
    steps = [(csv("lockout-account.csv", "lockout_email,lockout_password,wrong_password"), ()), (header_manager(), ()), (setup_url(), ())]
    for attempt in range(1, 4):
        steps.append((sampler(f"LOCKOUT_WRONG_{attempt}", "POST", "/api/login", '{"email":"${lockout_email}","password":"${wrong_password}"}'), [(status_assertion(401), ())]))
    steps.append((sampler("LOCKOUT_WHILE_LOCKED", "POST", "/api/login", '{"email":"${lockout_email}","password":"${lockout_password}"}'), [(status_assertion(403), ())]))
    return element, steps


def listener(guiclass, name):
    return make(
        "ResultCollector",
        {
            "guiclass": guiclass,
            "testclass": "ResultCollector",
            "testname": name,
            "enabled": "false",
        },
    )


def plan(kind):
    root = make("jmeterTestPlan", {"version": "1.2", "properties": "5.0", "jmeter": "5.6.3"})
    root_hash = child(root, "hashTree")
    element = make("TestPlan", {"guiclass": "TestPlanGui", "testclass": "TestPlan", "testname": f"{STUDENT_ID} {kind} performance plan", "enabled": "true"})
    prop(element, "stringProp", "TestPlan.comments", "Member 3 workflow; API review: https://github.com/ttbhanh/eshop-sut")
    prop(element, "boolProp", "TestPlan.functional_mode", "false")
    prop(element, "boolProp", "TestPlan.serialize_threadgroups", "false")
    args = child(element, "elementProp", {"name": "TestPlan.user_defined_variables", "elementType": "Arguments", "guiclass": "ArgumentsPanel", "testclass": "Arguments", "testname": "User Defined Variables", "enabled": "true"})
    collection = child(args, "collectionProp", {"name": "Arguments.arguments"})
    for name, value in (("baseUrl", "${__P(baseUrl,http://localhost:3000)}"), ("dataDir", "${__P(dataDir,data)}"), ("thinkMinMs", "${__P(thinkMinMs,1000)}"), ("thinkMaxMs", "${__P(thinkMaxMs,2000)}")):
        item = child(collection, "elementProp", {"name": name, "elementType": "Argument"})
        prop(item, "stringProp", "Argument.name", name)
        prop(item, "stringProp", "Argument.value", value)
        prop(item, "stringProp", "Argument.metadata", "=")
    if kind == "Load":
        children = [group("LOAD - 20 VU", "${__P(threads,20)}", "${__P(rampSeconds,60)}", "${__P(durationSeconds,360)}")]
        view = listener("ViewResultsFullVisualizer", "Load report view - View Results Tree")
    elif kind == "Stress":
        children = [group("STRESS - 100 VU", "${__P(threads,100)}", "${__P(rampSeconds,300)}", "${__P(durationSeconds,480)}")]
        view = listener("SummaryReport", "Stress report view - Summary Report")
    else:
        children = [group("SPIKE - background", "${__P(backgroundThreads,10)}", "${__P(backgroundRampSeconds,60)}", "${__P(backgroundDurationSeconds,420)}", input_file="per-vu/input-${__threadNum}.csv"), group("SPIKE - burst", "${__P(spikeThreads,90)}", "${__P(spikeRampSeconds,5)}", "${__P(spikeDurationSeconds,120)}", "${__P(spikeDelaySeconds,120)}", input_file="per-vu/input-${__intSum(${__threadNum},10)}.csv")]
        view = listener("StatVisualizer", "Spike report view - Aggregate Report")
    children.extend([lockout_group(), (view, ())])
    pair(root_hash, element, children)
    return ET.ElementTree(root)


def main():
    for kind in ("Load", "Stress", "Spike"):
        tree = plan(kind)
        path = OUT / f"{STUDENT_ID}_{kind}_{RUN_DATE}.jmx"
        ET.indent(tree, space="  ")
        tree.write(path, encoding="UTF-8", xml_declaration=True)
        print(path)


if __name__ == "__main__":
    main()
