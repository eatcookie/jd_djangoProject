$(function () {



    // r-chart 002   #f41127
    // 总评数和视频晒单数//折线图
    var optionsLine = {

        series: [{
			name: "总评数",
            type: "line",
			data: [3000, 2500, 5600, 3000, 2030, 1270]
		}, {
			name: "视频晒单数",
            type: "line",
			data: [300, 330, 210, 420, 190, 320]
		}],

		chart: {
			foreColor: '#9ba7b2',
			height: 360,
			type: 'line',
			zoom: {
				enabled: true
			},
			dropShadow: {
				enabled: true,
				top: 3,
				left: 2,
				blur: 4,
				opacity: 0.1,
			},
            toolbar: {
                show: true    //就是右上的三条横线的样式类似数字"三"的可点击图标,false是关，true是开
            },
		},

		stroke: {
			curve: 'smooth',
			width: 5
		},

        // plotOptions: {
        //     line: {
        //         columnWidth: '35%',
        //         endingShape: 'rounded'
        //     }
        // },

		colors: ["#0d6efd", '#f41127'],

		title: {
			text: 'CommentCountStr and VideoCountStr Chart',
			align: 'left',
			offsetY: 25,
			offsetX: 20
		},

        dataLabels: {
            enabled: true, // 启用数据标签
            enabledOnSeries: [0] // 数据标签0是只在第一个系列上显示，数据标签1是只在第二个系列上显示
        },

        // labels: [ '荣耀（HONOR）', '华为（HUAWEI）', '小米（MI）', 'vivo', '真我（realme）', 'OPPO'],

        xaxis: {
            categories: ['荣耀（HONOR）', '华为（HUAWEI）', '小米（MI）', 'vivo', '真我（realme）', 'OPPO'],
        },

        yaxis: [
            {
                title: {
                    text: '总评数',
                },
                opposite: false, // 默认放置在左侧
                seriesNames: ['总评数'], // 指定此Y轴适用于哪些系列
                max: 8000, // 设置最大值
                min: 0,
            },
            {
                title: {
                    text: '视频晒单数',
                },
                opposite: true, // 放置在右侧
                seriesNames: ['视频晒单数'], // 指定此Y轴适用于哪个系列
                max: 500, // 设置最大值
                min: 0,

            }
        ],

        //
        //
        // xaxis: {
		// 	tooltip: {
		// 		enabled: false
		// 	}
		// },

		// legend: {
		// 	position: 'bottom',
		// 	horizontalAlign: 'middle',
		// 	offsetY: -20
		// }

	}
	var chart = new ApexCharts(document.querySelector('#r-chart002'), optionsLine);
	chart.render();




    // r-chart 1
    // 评论分布//柱状图
    var options = {
        series: [
            {
                name: '好评',
                type: 'column', // 明确指定类型为柱状图
                data: [960, 850, 1310, 1080, 870, 605]
            },
            {
                name: '中评',
                type: 'column', // 明确指定类型为柱状图
                data: [440, 250, 507, 406, 601, 508]
            },

            {
                name: '差评',
                type: 'column', // 明确指定类型为柱状图
                data: [135, 141, 66, 126, 245, 148],

            }
        ],
        chart: {
            foreColor: '#9ba7b2',
            type: 'bar', // 明确图表类型为bar
            height: 360,
            stacked: false, // 确保不是堆叠柱状图
            toolbar: {
                show: true // 可选，隐藏工具栏,就是右上的三条横线的样式类似数字"三"的可点击图标
            }
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '75%',
                endingShape: 'rounded'
            },
        },
        colors: ["#f41127", '#0d6efd', '#ffc107'],
        title: {
			text: 'GoodCountStr and GeneralCountStr and PoorCountStr Chart',
			align: 'left',
			offsetY: 25,
			offsetX: 20
		},

        xaxis: {
            categories: ['荣耀（HONOR）', '华为（HUAWEI）', '小米（MI）', 'vivo', '真我（realme）', 'OPPO'],
        },

        yaxis: [
            {
                title: {
                    text: '好评和中评和差评',
                },
                opposite: false, // 默认放置在左侧
                seriesNames: ['好评和中评和差评'], // 指定此Y轴适用于哪些系列
                max: 1500, // 设置最大值
            },
            // {
            //     title: {
            //         text: '中评',
            //     },
            //     opposite: false, // 默认放置在左侧
            //     seriesNames: [ '中评'], // 指定此Y轴适用于哪些系列
            //     max: 1200, // 设置最大值
            // },
            // {
            //     title: {
            //         text: '差评',
            //     },
            //     opposite: true, // 放置在右侧
            //     seriesNames: ['差评'], // 指定此Y轴适用于哪个系列
            //     max: 100, // 设置最大值
            //
            // }
        ],
    };
    var chart = new ApexCharts(document.querySelector("#r-chart1"), options);
    chart.render();




    // r-chart 2
    // 销售额排行榜//水平柱状图
    var options = {
        series: [{
            data: [800, 730, 648, 570, 540, 480, 390, 310, 300, 280]
        }],
        chart: {
            foreColor: '#9ba7b2',
            type: 'bar',
            height: 350
        },
        colors: ["#ffc107"],
        title: {
			text: 'CommentCountStr multiply Price Chart',
			align: 'left',
			offsetY: 25,
			offsetX: 20
		},
        plotOptions: {       //plotOptions绘图选项
            bar: {
                horizontal: true,  //horizontal水平的，例如柱状图，如果true是水平柱状图，如果是false是非水平柱状图(即普通的正常的垂直的柱状图)
                columnWidth: '15%',
                endingShape: 'rounded'
            }
        },
        dataLabels: {
            enabled: false,
        },
        xaxis: {
            categories: ['荣耀（HONOR）', '华为（HUAWEI）', '小米（MI）', 'vivo', '真我（realme）', 'OPPO'],
        }
    };
    var chart = new ApexCharts(document.querySelector("#r-chart2"), options);
    chart.render();




    // r-chart 3
    // 销量和好评率//柱状图与折线图的混合图/组合图
    var options = {
        series: [{
            name: '销量',
            type: 'column',
            data: [440, 505, 714, 671, 227, 413]
        }, {
            name: '好评率',
            type: 'line',
            data: [0.93, 0.91, 0.98, 0.95, 0.93, 0.94]
        }],
        chart: {
            foreColor: '#9ba7b2',
            height: 350,
            type: 'line',
            zoom: {
                enabled: false
            },
            toolbar: {
                show: true
            },
        },
        stroke: {
            width: [0, 4] // 定义每个系列的线条宽度，第一个系列设为0表示柱状，第二个为4表示折线
        },
        plotOptions: {
            bar: {
                columnWidth: '25%',
                endingShape: 'rounded'
            }
        },
        colors: ["#f41127", "#0d6efd"],
        title: {
			text: 'CommentCountStr and GoodRate Chart',
			align: 'left',
			offsetY: 25,
			offsetX: 20
		},
        dataLabels: {
            enabled: false, // 是否启用数据标签
            enabledOnSeries: [1], // 数据标签只在第二个系列上显示
        },
        labels: ['荣耀（HONOR）', '华为（HUAWEI）', '小米（MI）', 'vivo', '真我（realme）', 'OPPO'],
        yaxis: [
            {
            title: {
                text: '销量',
            },
        },

            {
            opposite: true,
            title: {
                text: '好评率'
            },
            min: 0.9 // 设置 y 轴最小值为 0.9
        },
        ],

        xaxis:
            {
                title: {
                    text: '品牌',
                },
            }

    };
    var chart = new ApexCharts(document.querySelector("#r-chart3"), options);
    chart.render();




    // r-chart 4
    // 多维度对比//雷达图
    var options = {
        series: [{
            name: '荣耀（HONOR）',
            data: [80, 50, 30, 40, 43],
        }, {
            name: '华为（HUAWEI）',
            data: [90, 90, 40, 80, 20],
        }, {
            name: '小米（MI）',
            data: [44, 76, 78, 13, 100],
        }],
        chart: {
            foreColor: '#9ba7b2',
            height: 350,
            type: 'radar',
            dropShadow: {
                enabled: true,
                blur: 1,
                left: 1,
                top: 1
            },
            toolbar: {
                show: true
            },
        },
        colors: ["#17a00e", "#f41127", "#ff9000"],
        title: {
			text: 'Multi-Dimensional Chart',
			align: 'left',
			offsetY: 25,
			offsetX: 20
		},
        stroke: {
            width: 2
        },
        fill: {
            opacity: 0.1
        },
        markers: {
            size: 0
        },
        xaxis: {
            categories: ['价格', '销量', '好评率', '追评率', '商品量']
        }
    };
    var chart = new ApexCharts(document.querySelector("#r-chart4"), options);
    chart.render();







    // r-chart-learn-1//
        // 折线图（Line Chart）：适用于展示趋势。
        // 柱状图（Bar Chart）：适用于比较不同类别的数据。
        // 饼图（Pie Chart）：适用于展示部分与整体的关系。
        // 雷达图（Radar Chart）：适用于多维数据的比较。
        // 混合图（Mixed Chart）：可以组合多种图表类型（如柱状图和折线图）。
    var options = {
        //系列（series）：定义图表的数据系列，包括name名称、类型type和数据data。
        series: [{
            name: '荣耀（HONOR）',
            data: [80, 50, 30, 40, 43],
        }, {
            name: '华为（HUAWEI）',
            data: [90, 90, 40, 80, 20],
        }, {
            name: '小米（MI）',
            data: [44, 76, 78, 13, 100],
        }],
        // 图表配置（chart）：设置图表的type类型、height高度、toolbar工具栏等。
        // 自定义配置：
            // 工具栏（toolbar）：可以显示或隐藏图表的工具栏。
            // 阴影（dropShadow）：为图表添加阴影效果。
            // 响应式设计（responsive）：确保图表在不同设备上自适应显示。
            // 交互功能（interaction）：支持鼠标悬停、点击等交互事件。
        // 交互功能：
            // 悬停提示（tooltip）：显示数据点的详细信息。
            // 点击事件（click）：监听图表的点击事件。
            // 缩放（zoom）：支持图表的缩放功能。
        chart: {
            foreColor: '#9ba7b2',
            height: 350,
            type: 'radar',
            dropShadow: {
                enabled: true,
                blur: 1,
                left: 1,
                top: 1
            },
            zoom: {
                enabled: false
            },
            toolbar: {
                show: true
            },},

        //坐标轴（xaxis, yaxis）：定义 x 轴和 y 轴的标签、范围等。
        xaxis: {
            categories: ['荣耀（HONOR）', '华为（HUAWEI）', '小米（MI）', 'vivo', '真我（realme）', 'OPPO'],
        },
        yaxis: [
            {title: {
                    text: '好评和中评和差评',
                },
                opposite: false, // 默认放置在左侧
                seriesNames: ['好评和中评和差评'], // 指定此Y轴适用于哪些系列
                max: 1500, // 设置最大值
                min: 10,
            }],
        //颜色（colors）：自定义图表的颜色。
        colors: ["#17a00e", "#f41127", "#ff9000"],
        //标题（title）：设置图表的标题。
        title: {
			text: 'Multi-dimensional Chart',
			align: 'left',
			offsetY: 25,
			offsetX: 20
		},
        //数据标签（dataLabels）：控制是否显示数据标签及其位置。
        dataLabels: {
            enabled: true, // 启用数据标签
            enabledOnSeries: [1] // 数据标签只在第二个系列上显示
            },
        //标记（markers）：定义数据点的样式。
        markers: {
			size: 4,
			strokeWidth: 0,
			hover: {size: 7},
		},
        //网格（grid）：设置网格线的样式。
        grid: {
			show: true,
			padding: {bottom: 0}
		},
        //图例（legend）：控制图例的显示位置和样式。
        labels: ['荣耀（HONOR）', '华为（HUAWEI）', '小米（MI）', 'vivo', '真我（realme）', 'OPPO'],

		// subtitle: {
		// 	text: 'hello',
		// 	offsetY: 55,
		// 	offsetX: 20
		// },



        // stroke: {
        //     width: 2
        // },
        // fill: {
        //     opacity: 0.1
        // },

        // xaxis: {
        //     categories: ['价格', '销量', '好评率', '追评率', '商品量']
        // }
    };
    var chart = new ApexCharts(document.querySelector("#r-chart-learn-1"), options);
    chart.render();









});