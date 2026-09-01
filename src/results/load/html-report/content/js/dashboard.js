/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
var showControllersOnly = false;
var seriesFilter = "";
var filtersOnlySampleSeries = true;

/*
 * Add header in statistics table to group metrics by category
 * format
 *
 */
function summaryTableHeader(header) {
    var newRow = header.insertRow(-1);
    newRow.className = "tablesorter-no-sort";
    var cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Requests";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 3;
    cell.innerHTML = "Executions";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 7;
    cell.innerHTML = "Response Times (ms)";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Throughput";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 2;
    cell.innerHTML = "Network (KB/sec)";
    newRow.appendChild(cell);
}

/*
 * Populates the table identified by id parameter with the specified data and
 * format
 *
 */
function createTable(table, info, formatter, defaultSorts, seriesIndex, headerCreator) {
    var tableRef = table[0];

    // Create header and populate it with data.titles array
    var header = tableRef.createTHead();

    // Call callback is available
    if(headerCreator) {
        headerCreator(header);
    }

    var newRow = header.insertRow(-1);
    for (var index = 0; index < info.titles.length; index++) {
        var cell = document.createElement('th');
        cell.innerHTML = info.titles[index];
        newRow.appendChild(cell);
    }

    var tBody;

    // Create overall body if defined
    if(info.overall){
        tBody = document.createElement('tbody');
        tBody.className = "tablesorter-no-sort";
        tableRef.appendChild(tBody);
        var newRow = tBody.insertRow(-1);
        var data = info.overall.data;
        for(var index=0;index < data.length; index++){
            var cell = newRow.insertCell(-1);
            cell.innerHTML = formatter ? formatter(index, data[index]): data[index];
        }
    }

    // Create regular body
    tBody = document.createElement('tbody');
    tableRef.appendChild(tBody);

    var regexp;
    if(seriesFilter) {
        regexp = new RegExp(seriesFilter, 'i');
    }
    // Populate body with data.items array
    for(var index=0; index < info.items.length; index++){
        var item = info.items[index];
        if((!regexp || filtersOnlySampleSeries && !info.supportsControllersDiscrimination || regexp.test(item.data[seriesIndex]))
                &&
                (!showControllersOnly || !info.supportsControllersDiscrimination || item.isController)){
            if(item.data.length > 0) {
                var newRow = tBody.insertRow(-1);
                for(var col=0; col < item.data.length; col++){
                    var cell = newRow.insertCell(-1);
                    cell.innerHTML = formatter ? formatter(col, item.data[col]) : item.data[col];
                }
            }
        }
    }

    // Add support of columns sort
    table.tablesorter({sortList : defaultSorts});
}

$(document).ready(function() {

    // Customize table sorter default options
    $.extend( $.tablesorter.defaults, {
        theme: 'blue',
        cssInfoBlock: "tablesorter-no-sort",
        widthFixed: true,
        widgets: ['zebra']
    });

    var data = {"OkPercent": 100.0, "KoPercent": 0.0};
    var dataset = [
        {
            "label" : "FAIL",
            "data" : data.KoPercent,
            "color" : "#FF6347"
        },
        {
            "label" : "PASS",
            "data" : data.OkPercent,
            "color" : "#9ACD32"
        }];
    $.plot($("#flot-requests-summary"), dataset, {
        series : {
            pie : {
                show : true,
                radius : 1,
                label : {
                    show : true,
                    radius : 3 / 4,
                    formatter : function(label, series) {
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                            + label
                            + '<br/>'
                            + Math.round10(series.percent, -2)
                            + '%</div>';
                    },
                    background : {
                        opacity : 0.5,
                        color : '#000'
                    }
                }
            }
        },
        legend : {
            show : true
        }
    });

    // Creates APDEX table
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [1.0, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/51)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/35)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/47)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/15)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/27)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/31)"], "isController": false}, {"data": [1.0, 500, 1500, "2. Read - Get Admin Users (GET /api/admin/users)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/43)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/11)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/55)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/23)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/9)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/28)"], "isController": false}, {"data": [1.0, 500, 1500, "5. Transactional - Create Product (POST /api/products)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/50)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/30)"], "isController": false}, {"data": [1.0, 500, 1500, "1. Auth - Admin Login (POST /api/login)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/46)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/14)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/26)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/38)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/42)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/10)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/54)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/22)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/34)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/8)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/39)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/19)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/41)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/13)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/25)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/37)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/49)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/53)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/21)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/33)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/45)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/7)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/18)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/40)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/52)"], "isController": false}, {"data": [1.0, 500, 1500, "3. Read - Get Products List (GET /api/products)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/24)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/36)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/48)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/16)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/20)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/32)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/44)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/12)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/6)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/17)"], "isController": false}, {"data": [1.0, 500, 1500, "6. Transactional - Delete Product Cleanup (DELETE /api/products/29)"], "isController": false}, {"data": [1.0, 500, 1500, "4. Read - Get Categories (GET /api/categories)"], "isController": false}]}, function(index, item){
        switch(index){
            case 0:
                item = item.toFixed(3);
                break;
            case 1:
            case 2:
                item = formatDuration(item);
                break;
        }
        return item;
    }, [[0, 0]], 3);

    // Create statistics table
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 300, 0, 0.0, 10.073333333333334, 3, 102, 8.0, 17.0, 18.0, 23.99000000000001, 5.055952541458811, 2.8404677124764057, 1.144370091512741], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/51)", 1, 0, 0.0, 14.0, 14, 14, 14.0, 14.0, 14.0, 14.0, 71.42857142857143, 18.694196428571427, 12.555803571428571], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/35)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 10.986328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/47)", 1, 0, 0.0, 14.0, 14, 14, 14.0, 14.0, 14.0, 14.0, 71.42857142857143, 18.694196428571427, 12.555803571428571], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/15)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.71875], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/27)", 1, 0, 0.0, 14.0, 14, 14, 14.0, 14.0, 14.0, 14.0, 71.42857142857143, 18.694196428571427, 12.555803571428571], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/31)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 10.986328125], "isController": false}, {"data": ["2. Read - Get Admin Users (GET /api/admin/users)", 50, 0, 0.0, 6.96, 3, 15, 7.0, 8.0, 11.349999999999987, 15.0, 0.9555479111722661, 0.4712418897871039, 0.29580926547032066], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/43)", 1, 0, 0.0, 18.0, 18, 18, 18.0, 18.0, 18.0, 18.0, 55.55555555555555, 14.539930555555557, 9.765625], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/11)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 10.986328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/55)", 1, 0, 0.0, 13.0, 13, 13, 13.0, 13.0, 13.0, 13.0, 76.92307692307693, 20.13221153846154, 13.521634615384617], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/23)", 1, 0, 0.0, 14.0, 14, 14, 14.0, 14.0, 14.0, 14.0, 71.42857142857143, 18.694196428571427, 12.555803571428571], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/9)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.282628676470587], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/28)", 1, 0, 0.0, 18.0, 18, 18, 18.0, 18.0, 18.0, 18.0, 55.55555555555555, 14.539930555555557, 9.765625], "isController": false}, {"data": ["5. Transactional - Create Product (POST /api/products)", 50, 0, 0.0, 15.780000000000001, 10, 23, 16.0, 18.0, 20.799999999999983, 23.0, 0.9885721064494444, 0.26637384337063547, 0.34341295869745736], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/50)", 1, 0, 0.0, 12.0, 12, 12, 12.0, 12.0, 12.0, 12.0, 83.33333333333333, 21.809895833333332, 14.6484375], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/30)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 10.986328125], "isController": false}, {"data": ["1. Auth - Admin Login (POST /api/login)", 50, 0, 0.0, 10.399999999999997, 3, 102, 8.0, 11.0, 26.999999999999915, 102.0, 1.016053647632595, 0.607250812842918, 0.22424621520016255], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/46)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 10.986328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/14)", 1, 0, 0.0, 12.0, 12, 12, 12.0, 12.0, 12.0, 12.0, 83.33333333333333, 21.809895833333332, 14.6484375], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/26)", 1, 0, 0.0, 12.0, 12, 12, 12.0, 12.0, 12.0, 12.0, 83.33333333333333, 21.809895833333332, 14.6484375], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/38)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.71875], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/42)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.340073529411764], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/10)", 1, 0, 0.0, 11.0, 11, 11, 11.0, 11.0, 11.0, 11.0, 90.9090909090909, 23.792613636363637, 15.980113636363637], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/54)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.71875], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/22)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 10.986328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/34)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.71875], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/8)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.282628676470587], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/39)", 1, 0, 0.0, 14.0, 14, 14, 14.0, 14.0, 14.0, 14.0, 71.42857142857143, 18.694196428571427, 12.555803571428571], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/19)", 1, 0, 0.0, 13.0, 13, 13, 13.0, 13.0, 13.0, 13.0, 76.92307692307693, 20.13221153846154, 13.521634615384617], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/41)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 10.986328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/13)", 1, 0, 0.0, 10.0, 10, 10, 10.0, 10.0, 10.0, 10.0, 100.0, 26.171875, 17.578125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/25)", 1, 0, 0.0, 19.0, 19, 19, 19.0, 19.0, 19.0, 19.0, 52.63157894736842, 13.774671052631579, 9.251644736842106], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/37)", 1, 0, 0.0, 10.0, 10, 10, 10.0, 10.0, 10.0, 10.0, 100.0, 26.171875, 17.578125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/49)", 1, 0, 0.0, 13.0, 13, 13, 13.0, 13.0, 13.0, 13.0, 76.92307692307693, 20.13221153846154, 13.521634615384617], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/53)", 1, 0, 0.0, 13.0, 13, 13, 13.0, 13.0, 13.0, 13.0, 76.92307692307693, 20.13221153846154, 13.521634615384617], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/21)", 1, 0, 0.0, 12.0, 12, 12, 12.0, 12.0, 12.0, 12.0, 83.33333333333333, 21.809895833333332, 14.6484375], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/33)", 1, 0, 0.0, 24.0, 24, 24, 24.0, 24.0, 24.0, 24.0, 41.666666666666664, 10.904947916666666, 7.32421875], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/45)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.71875], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/7)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.282628676470587], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/18)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.71875], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/40)", 1, 0, 0.0, 14.0, 14, 14, 14.0, 14.0, 14.0, 14.0, 71.42857142857143, 18.694196428571427, 12.555803571428571], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/52)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.71875], "isController": false}, {"data": ["3. Read - Get Products List (GET /api/products)", 50, 0, 0.0, 6.239999999999999, 4, 10, 6.0, 7.899999999999999, 8.0, 10.0, 0.9581297307655456, 1.3668506575165276, 0.14502940260611286], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/24)", 1, 0, 0.0, 13.0, 13, 13, 13.0, 13.0, 13.0, 13.0, 76.92307692307693, 20.13221153846154, 13.521634615384617], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/36)", 1, 0, 0.0, 17.0, 17, 17, 17.0, 17.0, 17.0, 17.0, 58.8235294117647, 15.395220588235293, 10.340073529411764], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/48)", 1, 0, 0.0, 14.0, 14, 14, 14.0, 14.0, 14.0, 14.0, 71.42857142857143, 18.694196428571427, 12.555803571428571], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/16)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 10.986328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/20)", 1, 0, 0.0, 19.0, 19, 19, 19.0, 19.0, 19.0, 19.0, 52.63157894736842, 13.774671052631579, 9.251644736842106], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/32)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.71875], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/44)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 10.986328125], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/12)", 1, 0, 0.0, 13.0, 13, 13, 13.0, 13.0, 13.0, 13.0, 76.92307692307693, 20.13221153846154, 13.521634615384617], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/6)", 1, 0, 0.0, 16.0, 16, 16, 16.0, 16.0, 16.0, 16.0, 62.5, 16.357421875, 10.92529296875], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/17)", 1, 0, 0.0, 15.0, 15, 15, 15.0, 15.0, 15.0, 15.0, 66.66666666666667, 17.447916666666668, 11.71875], "isController": false}, {"data": ["6. Transactional - Delete Product Cleanup (DELETE /api/products/29)", 1, 0, 0.0, 14.0, 14, 14, 14.0, 14.0, 14.0, 14.0, 71.42857142857143, 18.694196428571427, 12.555803571428571], "isController": false}, {"data": ["4. Read - Get Categories (GET /api/categories)", 50, 0, 0.0, 6.120000000000001, 3, 9, 6.0, 8.0, 8.449999999999996, 9.0, 0.9750199879097522, 0.31421542579122874, 0.14949036924006942], "isController": false}]}, function(index, item){
        switch(index){
            // Errors pct
            case 3:
                item = item.toFixed(2) + '%';
                break;
            // Mean
            case 4:
            // Mean
            case 7:
            // Median
            case 8:
            // Percentile 1
            case 9:
            // Percentile 2
            case 10:
            // Percentile 3
            case 11:
            // Throughput
            case 12:
            // Kbytes/s
            case 13:
            // Sent Kbytes/s
                item = item.toFixed(2);
                break;
        }
        return item;
    }, [[0, 0]], 0, summaryTableHeader);

    // Create error table
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": []}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 300, 0, "", "", "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
