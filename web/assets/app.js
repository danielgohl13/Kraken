var vm = new Vue({
    el: '#app',
    components: {
        apexchart: VueApexCharts,
    },
    data: {
        capLoading: false,
        fab: false,
        settingsValid: true,
        settingsDialog: false,
        sizeSplit: 'default', //TODO: get from saved settings
        smThreshold: null, //TODO: get from saved settings
        mdThreshold: null, //TODO: get from saved settings
        streamDialog: false,
        inputDialog: false,
        camload: false,
        quantity: 0,
        accuracy: 0,
        size: 0,
        streamIp: "",
        streamIndeterminate: false,
        capProgress: 0,
        streamTime: 0,

        series: [{
            name: 'Quantidade',
            data: []
        }, {
            name: 'Acurácia',
            data: []
        },],
        chartOptions: {
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '60%',
                },
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                show: true,
                width: 2,
                colors: ['transparent']
            },

            xaxis: {
                categories: ['Pequenos', 'Médios', 'Grandes'],
            },
            yaxis: [{
                title: {
                    text: 'Quantidade'
                },
                decimalsInFloat: 0,
            }, {
                opposite: true,
                title: {
                    text: 'Acurácia (%)'
                },
                decimalsInFloat: 0,
            }],
            fill: {
                opacity: 1

            },
            tooltip: {
                y: [{
                    formatter: function (val) {
                        return val + " peixes"
                    }
                }, {
                    formatter: function (val) {
                        return val.toFixed(2) + "%"
                    }
                }]
            }
        }
    },
    methods: {
        open_url(url) {
            window.open(url, "_blank");
        },

        startCapture() {
            var me = this;
            this.capLoading = true;
            this.streamIndeterminate = false;
            this.capProgress = 0;

            var interval = setInterval(() => {
                if (this.capProgress >= 100) {
                    this.streamIndeterminate = true;
                    clearInterval(interval);
                }
                this.capProgress += 5;
            }, 250) //TODO: change to fit duration*50

            var source = new EventSource('/cap?ip=' + this.streamIp + ":8080" + "&timestamp=" + new Date().getTime());
            source.onmessage = function (event) {
                if (event.data == 100) {
                    me.capLoading = false;
                    me.streamDialog = false;
                    me.parse();
                    clearInterval(interval);
                }
            }

        },

        sendFile() {
            this.capLoading = true;
            this.streamIndeterminate = false;
            this.capProgress = 0

            var formData = new FormData();
            var videoFile = document.querySelector('#file');
            formData.append("file", videoFile.files[0]);
            axios.post('/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
                onUploadProgress: progressEvent => {
                    this.capProgress = (progressEvent.loaded / progressEvent.total) * 100
                    if (this.capProgress >= 100) {
                        this.streamIndeterminate = true;
                    }
                }
            }).then(response => {
                this.capLoading = false;
                this.inputDialog = false;
                this.parse();
            })

        },

        validate() {
            return this.$refs.form.validate();
        },

        saveSettings() {
            if (this.validate()) {
                this.parse();
                this.settingsDialog = false;
            }
        },

        parse() {
            Papa.parse("assets/report.csv?timestamp=" + new Date().getTime(), {
                download: true,
                header: true,
                dynamicTyping: true,
                complete: function (results) {
                    vm.quantity = results.data.length;
                    var maxFish = Math.max.apply(Math, results.data.map(function (o) {
                        return o.x * o.y;
                    }));

                    var smThreshold = (vm.sizeSplit == 'custom') ? vm.smThreshold / 100 : null || maxFish / 3;
                    var mdThreshold = (vm.sizeSplit == 'custom') ? vm.mdThreshold / 100 : null || 2 * maxFish / 3;

                    var fishs = results.data.filter(function (f) {
                        return f.x * f.y < smThreshold;
                    });

                    var fishm = results.data.filter(function (f) {
                        var area = f.x * f.y;
                        return (area >= smThreshold) && (area < mdThreshold);
                    });

                    var fishl = results.data.filter(function (f) {
                        var area = f.x * f.y;
                        return area > mdThreshold;
                    });

                    vm.accuracy = accAvg(results.data).toFixed(2) + "%";
                    vm.size = sizAvg(results.data).toFixed(2) + " cm²"

                    vm.series = [
                        //  Quantidade
                        {
                            data: [fishs.length, fishm.length, fishl.length]
                        },
                        // Acurácia
                        { //        P   M   G
                            data: [accAvg(fishs), accAvg(fishm), accAvg(fishl)]
                        },
                    ];

                    vm.chartOptions = {
                        xaxis: {
                            categories: [
                                'Pequenos (<' + (smThreshold * 100).toFixed(1) + 'cm²)',
                                'Médios (<=' + (mdThreshold * 100).toFixed(1) + 'cm²)',
                                'Grandes (>' + (mdThreshold * 100).toFixed(1) + 'cm²)'
                            ],
                        },
                    };
                }
            });
        }

    }
});

var accAvg = function (fisharr) {
    var total = 0;
    for (let i = 0; i < fisharr.length; i++) {
        const f = fisharr[i];
        total += f.accuracy;
    }

    if (total == 0)
        return 0;
    else {
        return total * 100 / fisharr.length;
    }
}

var sizAvg = function (fisharr) {
    var total = 0;
    for (let i = 0; i < fisharr.length; i++) {
        const f = fisharr[i];
        total += f.x * f.y;
    }

    if (total == 0)
        return 0;
    else {
        return total * 100 / fisharr.length;
    }
}

vm.parse();


