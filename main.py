import sys
import os
import json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, 
    QCheckBox, QStackedWidget, QGridLayout, QScrollArea, 
    QSpinBox, QFormLayout, QLabel, QGroupBox, 
    QDialog, QDialogButtonBox, QVBoxLayout
)


class MainWindow(QMainWindow):
    pins = dict()
    pins["A"] = dict()
    pins["B"] = dict()
    pins["C"] = dict()
    pins["D"] = dict()
    pins["E"] = dict()
    
    lqfp100 = dict()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CH32V307 Pins")
        self.setMinimumSize(660, 500)
        
        self.stackedWidget = QStackedWidget()

        self.firstPageWidget = QWidget()
        self.initFirstPage()
        self.stackedWidget.addWidget(self.firstPageWidget)

        self.secondPageWidget = QWidget()
        self.secondPageLayout = QGridLayout()        
        self.secondPageWidget.setLayout(self.secondPageLayout)
        self.stackedWidget.addWidget(self.secondPageWidget)
        
        self.setCentralWidget(self.stackedWidget)
    

    def initFirstPage(self):
        firstPageLayout = QGridLayout()
        
        scrollArea = QScrollArea()
        scrollWidget = QWidget()
        self.scrollLayout = QGridLayout()
        self.scrollLayout.setVerticalSpacing(10)
        self.addModulesWidget()
        scrollWidget.setLayout(self.scrollLayout)
        scrollArea.setWidget(scrollWidget)

        bnReset = QPushButton("Сбросить")
        bnReset.clicked.connect(self.on_bnReset_pressed)

        bn = QPushButton("Разместить")
        bn.clicked.connect(self.on_bn_pressed)

        firstPageLayout.addWidget(scrollArea, 0, 0, 1, 2)
        firstPageLayout.addWidget(bnReset, 1, 0)
        firstPageLayout.addWidget(bn, 1, 1)
        self.firstPageWidget.setLayout(firstPageLayout)


    def addModulesWidget(self):
        self.fsmc_widget = QCheckBox("FSMC")
        self.fsmc_widget.setMinimumWidth(120)
        self.fsmc_widget.stateChanged.connect(self.on_fsmc_widget_changed)
        self.scrollLayout.addWidget(self.fsmc_widget, 0, 0)

        self.dvp_widget = QCheckBox("DVP")
        self.dvp_widget.setMinimumWidth(120)
        self.dvp_widget.stateChanged.connect(self.on_dvp_widget_changed)
        self.scrollLayout.addWidget(self.dvp_widget, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.sdio_widget = QCheckBox("SDIO")
        self.sdio_widget.stateChanged.connect(self.on_sdio_widget_changed)
        self.sdio_widget.setMinimumWidth(120)
        self.scrollLayout.addWidget(self.sdio_widget, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        eth_mac_widget = QGroupBox("ETH MAC")
        eth_mac_layout = QFormLayout()

        self.eth_mii_widget = QCheckBox("ETH MII")
        self.eth_mii_widget.stateChanged.connect(self.on_eth_mii_widget_changed)
        eth_mac_layout.addWidget(self.eth_mii_widget)

        self.eth_rmii_widget = QCheckBox("ETH RMII")
        self.eth_rmii_widget.stateChanged.connect(self.on_eth_rmii_widget_changed)
        eth_mac_layout.addWidget(self.eth_rmii_widget)

        self.eth_rgmii_widget = QCheckBox("ETH RGMII")
        self.eth_rgmii_widget.stateChanged.connect(self.on_eth_rgmii_widget_changed)
        eth_mac_layout.addWidget(self.eth_rgmii_widget)

        self.eth_option_widget = QCheckBox("100M/Gigabit")
        eth_mac_layout.addWidget(self.eth_option_widget)

        eth_mac_widget.setLayout(eth_mac_layout)
        self.scrollLayout.addWidget(eth_mac_widget, 1, 0)

        self.eth_10M_PHY_widget = QCheckBox("ETH 10M PHY")
        self.scrollLayout.addWidget(self.eth_10M_PHY_widget, 2, 0)

        usb_widget = QGroupBox("USB")
        usb_layout = QFormLayout()

        self.usbhs_widget = QCheckBox("USBHS")
        self.usbhs_widget.stateChanged.connect(self.on_usbhs_widget_changed)
        usb_layout.addWidget(self.usbhs_widget)

        self.usbfs_widget = QCheckBox("USBFS")
        self.usbfs_widget.stateChanged.connect(self.on_usbfs_widget_changed)
        usb_layout.addWidget(self.usbfs_widget)

        usb_widget.setLayout(usb_layout)
        self.scrollLayout.addWidget(usb_widget, 1, 1)

        self.otg_fs_widget = QCheckBox("OTG FS")
        self.scrollLayout.addWidget(self.otg_fs_widget, 2, 1)

        self.hse_widget = QCheckBox("HSE")
        self.scrollLayout.addWidget(self.hse_widget, 3, 0)

        self.lse_widget = QCheckBox("LSE")
        self.scrollLayout.addWidget(self.lse_widget, 3, 1)

        self.wkup_widget = QCheckBox("WKUP")
        self.scrollLayout.addWidget(self.wkup_widget, 3, 2)

        self.mco_widget = QCheckBox("MCO")
        self.mco_widget.setMinimumWidth(120)
        self.scrollLayout.addWidget(self.mco_widget, 3, 3)

        self.swdio_widget = QCheckBox("SWDIO")
        self.scrollLayout.addWidget(self.swdio_widget, 4, 0)

        self.swclk_widget = QCheckBox("SWCLK")
        self.scrollLayout.addWidget(self.swclk_widget, 4, 1)

        self.boot1_widget = QCheckBox("BOOT1")
        self.scrollLayout.addWidget(self.boot1_widget, 4, 2)

        self.tamper_rtc_widget = QCheckBox("TAMPER-RTC")
        self.scrollLayout.addWidget(self.tamper_rtc_widget, 4, 3)
    
        gptm_widget = QGroupBox("GPTM")
        gptm_layout = QFormLayout()

        self.tim_2_widget = QCheckBox("TIM 2")
        gptm_layout.addRow(self.tim_2_widget)

        self.tim_3_4_widget = QSpinBox(minimum=0, maximum=2)
        self.tim_3_4_widget.setMinimumHeight(30)
        gptm_layout.addRow("TIM 3/4", self.tim_3_4_widget)

        self.tim_5_widget = QCheckBox("TIM 5")
        gptm_layout.addRow(self.tim_5_widget)

        gptm_widget.setLayout(gptm_layout)
        self.scrollLayout.addWidget(gptm_widget, 5, 0)

        adtm_widget = QGroupBox("ADTM")
        adtm_layout = QFormLayout()

        self.tim_1_8_10_widget = QSpinBox(minimum=0, maximum=3)
        self.tim_1_8_10_widget.setMinimumHeight(30)
        adtm_layout.addRow("TIM 1/8/10", self.tim_1_8_10_widget)

        self.tim_9_widget = QCheckBox("TIM 9")
        adtm_layout.addRow(self.tim_9_widget)

        adtm_widget.setLayout(adtm_layout)
        self.scrollLayout.addWidget(adtm_widget, 5, 1)

        adc_dac_opa_form_widget = QWidget()
        adc_dac_opa_form_layout = QFormLayout()

        self.adc_widget = QSpinBox(minimum=0, maximum=16)
        self.adc_widget.setFixedSize(40, 30)
        adc_dac_opa_form_layout.addRow("ADC", self.adc_widget)

        self.dac_widget = QSpinBox(minimum=0, maximum=2)
        self.dac_widget.setFixedSize(40, 30)
        adc_dac_opa_form_layout.addRow("DAC", self.dac_widget)

        self.opa_widget = QSpinBox(minimum=0, maximum=4)
        self.opa_widget.setFixedSize(40, 30)
        adc_dac_opa_form_layout.addRow("OPA", self.opa_widget)

        adc_dac_opa_form_widget.setLayout(adc_dac_opa_form_layout)
        self.scrollLayout.addWidget(adc_dac_opa_form_widget, 5, 2)

        interfaces_widget = QWidget()
        interfaces_layout = QFormLayout()

        self.spi_widget = QSpinBox(minimum=0, maximum=3)
        self.spi_widget.setFixedSize(40, 30)
        interfaces_layout.addRow("SPI", self.spi_widget)

        self.i2s_widget = QSpinBox(minimum=0, maximum=2)
        self.i2s_widget.setFixedSize(40, 30)
        interfaces_layout.addRow("I2S", self.i2s_widget)

        self.i2c_widget = QSpinBox(minimum=0, maximum=2)
        self.i2c_widget.setFixedSize(40, 30)
        interfaces_layout.addRow("I2C", self.i2c_widget)

        self.can_widget = QSpinBox(minimum=0, maximum=2)
        self.can_widget.setFixedSize(40, 30)
        interfaces_layout.addRow("CAN", self.can_widget)

        interfaces_widget.setLayout(interfaces_layout)
        self.scrollLayout.addWidget(interfaces_widget, 1, 2)

        uart_usart_widget = QWidget()
        uart_usart_layout = QFormLayout()

        self.uart_widget = QSpinBox(minimum=0, maximum=8)
        self.uart_widget.setFixedSize(40, 30)
        self.uart_widget.valueChanged.connect(self.on_uart_widget_pressed)
        uart_usart_layout.addRow("UART", self.uart_widget)

        self.usart_widget = QSpinBox(minimum=0, maximum=3)
        self.usart_widget.setFixedSize(40, 30)
        self.usart_widget.valueChanged.connect(self.on_usart_widget_pressed)
        uart_usart_layout.addRow("USART", self.usart_widget)

        uart_usart_widget.setLayout(uart_usart_layout)
        self.scrollLayout.addWidget(uart_usart_widget, 1, 3)

        exti_gpio_form_widget = QWidget()
        exti_gpio_form_layout = QFormLayout()

        self.exti_widget = QSpinBox(minimum=0, maximum=16)
        self.exti_widget.setFixedSize(40, 30)
        exti_gpio_form_layout.addRow("EXTI", self.exti_widget)

        self.gpio_widget = QSpinBox(minimum=0, maximum=80)
        self.gpio_widget.setFixedSize(40, 30)
        exti_gpio_form_layout.addRow("GPIO", self.gpio_widget)

        exti_gpio_form_widget.setLayout(exti_gpio_form_layout)
        self.scrollLayout.addWidget(exti_gpio_form_widget, 5, 3)


    def on_fsmc_widget_changed(self, value):
        if Qt.CheckState(value) == Qt.CheckState.Checked:
            self.dvp_widget.setCheckState(Qt.CheckState.Unchecked)


    def on_dvp_widget_changed(self, value):
        if Qt.CheckState(value) == Qt.CheckState.Checked:
            self.fsmc_widget.setCheckState(Qt.CheckState.Unchecked)
            self.sdio_widget.setCheckState(Qt.CheckState.Unchecked)

    
    def on_sdio_widget_changed(self, value):
        if Qt.CheckState(value) == Qt.CheckState.Checked:
            self.dvp_widget.setCheckState(Qt.CheckState.Unchecked)


    def on_eth_mii_widget_changed(self, value):
        if Qt.CheckState(value) == Qt.CheckState.Checked:
            self.eth_rmii_widget.setCheckState(Qt.CheckState.Unchecked)
            self.eth_rgmii_widget.setCheckState(Qt.CheckState.Unchecked)


    def on_eth_rmii_widget_changed(self, value):
        if Qt.CheckState(value) == Qt.CheckState.Checked:
            self.eth_mii_widget.setCheckState(Qt.CheckState.Unchecked)
            self.eth_rgmii_widget.setCheckState(Qt.CheckState.Unchecked)


    def on_eth_rgmii_widget_changed(self, value):
        if Qt.CheckState(value) == Qt.CheckState.Checked:
            self.eth_mii_widget.setCheckState(Qt.CheckState.Unchecked)
            self.eth_rmii_widget.setCheckState(Qt.CheckState.Unchecked)


    def on_usbhs_widget_changed(self, value):
        if Qt.CheckState(value) == Qt.CheckState.Checked:
            self.usbfs_widget.setCheckState(Qt.CheckState.Unchecked)


    def on_usbfs_widget_changed(self, value):
        if Qt.CheckState(value) == Qt.CheckState.Checked:
            self.usbhs_widget.setCheckState(Qt.CheckState.Unchecked)


    def on_usart_widget_pressed(self, value):
        if self.uart_widget.value() > 5 and self.uart_widget.value() > 8 - value:
            self.uart_widget.setValue(8 - value)
    

    def on_uart_widget_pressed(self, value):
        if self.uart_widget.value() > 5 and self.usart_widget.value() > 8 - value:
            self.usart_widget.setValue(8 - value)


    def on_bnReset_pressed(self):
        self.fsmc_widget.setCheckState(Qt.CheckState.Unchecked)
        self.dvp_widget.setCheckState(Qt.CheckState.Unchecked)
        self.sdio_widget.setCheckState(Qt.CheckState.Unchecked)
        self.eth_mii_widget.setCheckState(Qt.CheckState.Unchecked)
        self.eth_rmii_widget.setCheckState(Qt.CheckState.Unchecked)
        self.eth_rgmii_widget.setCheckState(Qt.CheckState.Unchecked)
        self.eth_option_widget.setCheckState(Qt.CheckState.Unchecked)
        self.eth_10M_PHY_widget.setCheckState(Qt.CheckState.Unchecked)
        self.usbhs_widget.setCheckState(Qt.CheckState.Unchecked)
        self.usbfs_widget.setCheckState(Qt.CheckState.Unchecked)
        self.otg_fs_widget.setCheckState(Qt.CheckState.Unchecked)
        self.hse_widget.setCheckState(Qt.CheckState.Unchecked)
        self.lse_widget.setCheckState(Qt.CheckState.Unchecked)
        self.wkup_widget.setCheckState(Qt.CheckState.Unchecked)
        self.mco_widget.setCheckState(Qt.CheckState.Unchecked)
        self.swdio_widget.setCheckState(Qt.CheckState.Unchecked)
        self.swclk_widget.setCheckState(Qt.CheckState.Unchecked)
        self.boot1_widget.setCheckState(Qt.CheckState.Unchecked)
        self.tamper_rtc_widget.setCheckState(Qt.CheckState.Unchecked)
        self.tim_2_widget.setCheckState(Qt.CheckState.Unchecked)
        self.tim_3_4_widget.setValue(0)
        self.tim_5_widget.setCheckState(Qt.CheckState.Unchecked)
        self.tim_1_8_10_widget.setValue(0)
        self.tim_9_widget.setCheckState(Qt.CheckState.Unchecked)
        self.adc_widget.setValue(0)
        self.dac_widget.setValue(0)
        self.opa_widget.setValue(0)
        self.spi_widget.setValue(0)
        self.i2s_widget.setValue(0)
        self.i2c_widget.setValue(0)
        self.can_widget.setValue(0)
        self.usart_widget.setValue(0)
        self.uart_widget.setValue(0)
        self.exti_widget.setValue(0)
        self.gpio_widget.setValue(0)


    def on_bn_pressed(self):
        self.setMinimumSize(1000, 540)
        if not(self.windowState() & Qt.WindowState.WindowMaximized):
            self.resize(800, 440)
        self.updateSecondPage()
        self.stackedWidget.setCurrentIndex(1)


    def updateSecondPage(self):
        for i in reversed(range(self.secondPageLayout.count())): 
            self.secondPageLayout.itemAt(i).widget().setParent(None)
        
        self.initPins()
        wid = QWidget()
        self.wid_layout = QGridLayout()
        try:
            self.resolve_pins()
            self.add_pins_to_layout()
            wid.setLayout(self.wid_layout)

            bn2 = QPushButton("Назад")
            bn2.clicked.connect(self.on_bn2_pressed)

            bn3 = QPushButton("Результат размещения (LQFP100)")
            bn3.clicked.connect(self.on_bn3_pressed)

            bnSave = QPushButton("Cохранить результат размещения")
            bnSave.clicked.connect(self.on_bnSave_pressed)

            self.secondPageLayout.addWidget(wid, 0, 0, 1, 3)
            self.secondPageLayout.addWidget(bn2, 1, 0)
            self.secondPageLayout.addWidget(bn3, 1, 1)
            self.secondPageLayout.addWidget(bnSave, 1, 2)
            self.secondPageWidget.update()

        except Exception as exc:
            self.wid_layout.addWidget(QLabel(str(exc), alignment=Qt.AlignmentFlag.AlignTop))
            self.setMinimumSize(500, 120)
            if not(self.windowState() & Qt.WindowState.WindowMaximized):
                self.resize(400, 100)
            wid.setLayout(self.wid_layout)

            bn2 = QPushButton("Назад")
            bn2.clicked.connect(self.on_bn2_pressed)

            self.secondPageLayout.addWidget(wid, 0, 0)
            self.secondPageLayout.addWidget(bn2, 1, 0)
            self.secondPageWidget.update()


    def initPins(self):
        for i in range(0, 16):
            self.pins["A"][i] = "GPIO"
            self.pins["B"][i] = "GPIO"
            self.pins["C"][i] = "GPIO"
            self.pins["D"][i] = "GPIO"
            self.pins["E"][i] = "GPIO"


    def resolve_pins(self):
        if self.fsmc_widget.checkState() == Qt.CheckState.Checked:
            self.set_fsmc()
        if self.eth_mii_widget.checkState() == Qt.CheckState.Checked:
            self.set_eth_mii()
        if self.dvp_widget.checkState() == Qt.CheckState.Checked:
            self.set_dvp()
        if self.eth_rgmii_widget.checkState() == Qt.CheckState.Checked:
            self.set_eth_rgmii()
        if self.eth_rmii_widget.checkState() == Qt.CheckState.Checked:
            self.set_eth_rmii()
        if self.sdio_widget.checkState() == Qt.CheckState.Checked:
            self.set_sdio()
        if self.tim_5_widget.checkState() == Qt.CheckState.Checked:
            self.set_tim5()
        if self.eth_10M_PHY_widget.checkState() == Qt.CheckState.Checked:
            self.set_eth()
        if self.otg_fs_widget.checkState() == Qt.CheckState.Checked:
            self.set_otg_fs()
        if self.usbhs_widget.checkState() == Qt.CheckState.Checked:
            self.set_usbhs()
        if self.usbfs_widget.checkState() == Qt.CheckState.Checked:
            self.set_usbfs()
        if self.hse_widget.checkState() == Qt.CheckState.Checked:
            self.set_hse()
        if self.lse_widget.checkState() == Qt.CheckState.Checked:
            self.set_lse()
        if self.wkup_widget.checkState() == Qt.CheckState.Checked:
            if self.eth_mii_widget.checkState() == Qt.CheckState.Checked:
                raise Exception(f"Конфликт ETH MII и WKUP -> A0 = {self.pins['A'][0]}\n"
                    "Нельзя одновременно разместить ETH MII и WKUP")
            elif self.eth_rgmii_widget.checkState() == Qt.CheckState.Checked:
                raise Exception(f"Конфликт ETH RGMII и WKUP -> A0 = {self.pins['A'][0]}\n"
                    "Нельзя одновременно разместить ETH RGMII и WKUP")
            elif self.tim_5_widget.checkState() == Qt.CheckState.Checked:
                raise Exception(f"Конфликт TIM 5 и WKUP -> A0 = {self.pins['A'][0]}\n"
                    "Нельзя одновременно разместить TIM 5 и WKUP")
            else:
                self.pins['A'][0] = "WKUP"
        if self.mco_widget.checkState() == Qt.CheckState.Checked:
            self.pins['A'][8] = "MCO"
        if self.swdio_widget.checkState() == Qt.CheckState.Checked:
            self.pins['A'][13] = "SWDIO"
        if self.swclk_widget.checkState() == Qt.CheckState.Checked:
            self.pins['A'][14] = "SWCLK"
        if self.boot1_widget.checkState() == Qt.CheckState.Checked:
            self.pins['B'][2] = "BOOT1"
        if self.tamper_rtc_widget.checkState() == Qt.CheckState.Checked:
            self.pins['C'][13] = "TAMPER-RTC"
        if self.tim_9_widget.checkState() == Qt.CheckState.Checked:
            self.set_tim9()
        if self.tim_2_widget.checkState() == Qt.CheckState.Checked:
            self.set_tim2()
        self.set_dac(self.dac_widget.value())
        self.set_i2s(self.i2s_widget.value())
        self.set_i2c(self.i2c_widget.value())
        self.set_tim_3_4(self.tim_3_4_widget.value())
        self.set_can(self.can_widget.value())
        self.set_spi(self.spi_widget.value())
        self.set_tim_1_8_10(self.tim_1_8_10_widget.value())
        self.set_usart(self.usart_widget.value())
        self.set_opa(self.opa_widget.value())
        self.set_uart(self.uart_widget.value())
        self.set_adc(self.adc_widget.value())
        self.set_exti(self.exti_widget.value())
        self.set_gpio(self.gpio_widget.value())


    def set_fsmc(self):
        self.pins['D'][0]  = "FSMC_D2"
        self.pins['D'][1]  = "FSMC_D3"
        if self.usbhs_widget.checkState() == Qt.CheckState.Checked \
            or self.usbfs_widget.checkState() == Qt.CheckState.Checked:
            self.pins['D'][2]  = "FSMC_NADV"
        else:
            self.pins['B'][7]  = "FSMC_NADV"
        self.pins['D'][3]  = "FSMC_CLK"
        self.pins['D'][4]  = "FSMC_NOE"
        self.pins['D'][5]  = "FSMC_NWE"
        self.pins['D'][6]  = "FSMC_NWAIT"
        self.pins['D'][7]  = "FSMC_NE1_NCE2"
        self.pins['D'][8]  = "FSMC_D13"
        self.pins['D'][9]  = "FSMC_D14"
        self.pins['D'][10] = "FSMC_D15"
        self.pins['D'][11] = "FSMC_A16"
        self.pins['D'][12] = "FSMC_A17"
        self.pins['D'][13] = "FSMC_A18"
        self.pins['D'][14] = "FSMC_D0"
        self.pins['D'][15] = "FSMC_D1"
        self.pins['E'][0]  = "FSMC_NBL0"
        self.pins['E'][1]  = "FSMC_NBL1"
        self.pins['E'][2]  = "FSMC_A23"
        self.pins['E'][3]  = "FSMC_A19"
        self.pins['E'][4]  = "FSMC_A20"
        self.pins['E'][5]  = "FSMC_A21"
        self.pins['E'][6]  = "FSMC_A22"
        self.pins['E'][7]  = "FSMC_D4"
        self.pins['E'][8]  = "FSMC_D5"
        self.pins['E'][9]  = "FSMC_D6"
        self.pins['E'][10] = "FSMC_D7"
        self.pins['E'][11] = "FSMC_D8"
        self.pins['E'][12] = "FSMC_D9"
        self.pins['E'][13] = "FSMC_D10"
        self.pins['E'][14] = "FSMC_D11"
        self.pins['E'][15] = "FSMC_D12"


    def set_eth_mii(self):
        self.pins['A'][0]  = "ETH_MII_CRS_WKUP"
        self.pins['A'][1]  = "ETH_MII_RX_CLK"
        self.pins['A'][2]  = "ETH_MII_MDIO"
        self.pins['A'][3]  = "ETH_MII_COL"
        self.pins['A'][7]  = "ETH_MII_RX_DV"
        self.pins['B'][0]  = "ETH_MII_RXD2"
        self.pins['B'][1]  = "ETH_MII_RXD3"
        self.pins['B'][5]  = "ETH_MII_PPS_OUT"
        self.pins['B'][8]  = "ETH_MII_TXD3"
        self.pins['B'][10] = "ETH_MII_RX_ER"
        self.pins['B'][11] = "ETH_MII_TX_EN"
        self.pins['B'][12] = "ETH_MII_TXD0"
        self.pins['B'][13] = "ETH_MII_TXD1"
        self.pins['C'][1]  = "ETH_MII_MDC"
        self.pins['C'][2]  = "ETH_MII_TXD2"
        self.pins['C'][3]  = "ETH_MII_TX_CLK"
        self.pins['C'][4]  = "ETH_MII_RXD0"
        self.pins['C'][5]  = "ETH_MII_RXD1"


    def remap_eth_mii(self):
        if self.pins['D'][8] == "GPIO" and self.pins['D'][9] == "GPIO" \
           and self.pins['D'][10] == "GPIO" and self.pins['D'][11] == "GPIO" \
           and self.pins['D'][12] == "GPIO":
            
            self.pins['D'][8]  = self.pins['A'][7]
            self.pins['D'][9]  = self.pins['C'][4]
            self.pins['D'][10] = self.pins['C'][5]
            self.pins['D'][11] = self.pins['B'][0]
            self.pins['D'][12] = self.pins['B'][1]

            self.pins['A'][7] = "GPIO"
            self.pins['B'][0] = "GPIO"
            self.pins['B'][1] = "GPIO"
            self.pins['C'][4] = "GPIO"
            self.pins['C'][5] = "GPIO"
            return True
        else:
            return False


    def set_dvp(self):
        self.pins['A'][4]  = "DVP_HSYNC"
        self.pins['A'][5]  = "DVP_VSYNC"
        self.pins['A'][6]  = "DVP_PCLK"
        self.pins['A'][9]  = "DVP_D0"
        self.pins['A'][10] = "DVP_D1"
        if self.usbhs_widget.checkState() == Qt.CheckState.Checked \
            or self.usbfs_widget.checkState() == Qt.CheckState.Checked:
            self.pins['B'][3]  = "DVP_D5"
        else:
            self.pins['B'][6]  = "DVP_D5"
        if self.eth_mii_widget.checkState() == Qt.CheckState.Checked:
            raise Exception(f"Конфликт ETH MII и DVP -> B8 = {self.pins['B'][8]}\n"
                            "Нельзя одновременно разместить ETH MII и DVP")
        else:
            self.pins['B'][8]  = "DVP_D6"
        self.pins['B'][9]  = "DVP_D7"
        self.pins['C'][8]  = "DVP_D2"
        self.pins['C'][9]  = "DVP_D3"
        self.pins['C'][10] = "DVP_D8"
        self.pins['C'][11] = "DVP_D4"
        self.pins['C'][12] = "DVP_D9"
        self.pins['D'][2]  = "DVP_D11"
        self.pins['D'][6]  = "DVP_D10"


    def set_eth_rgmii(self):
        self.pins['A'][0] = "ETH_RGMII_RXD2"
        self.pins['A'][1] = "ETH_RGMII_RXD3"
        self.pins['A'][2] = "ETH_RGMII_GTXC"
        self.pins['A'][3] = "ETH_RGMII_TXEN"
        self.pins['A'][7] = "ETH_RGMII_TXD0"
        self.pins['B'][0] = "ETH_RGMII_TXD3"
        self.pins['B'][1] = "ETH_RGMII_125IN"
        self.pins['C'][0] = "ETH_RGMII_RXC"
        self.pins['C'][1] = "ETH_RGMII_RXCTL"
        self.pins['C'][2] = "ETH_RGMII_RXD0"
        self.pins['C'][3] = "ETH_RGMII_RXD1"
        self.pins['C'][4] = "ETH_RGMII_TXD1"
        self.pins['C'][5] = "ETH_RGMII_TXD2"


    def set_eth_rmii(self):
        self.pins['A'][1]  = "ETH_RMII_REF_CLK"
        self.pins['A'][2]  = "ETH_RMII_MDIO"
        self.pins['A'][7]  = "ETH_RMII_CRS_DV"
        self.pins['B'][5]  = "ETH_RMII_PPS_OUT"
        self.pins['B'][11] = "ETH_RMII_TX_EN"
        self.pins['B'][12] = "ETH_RMII_TXD0"
        self.pins['B'][13] = "ETH_RMII_TXD1"
        self.pins['C'][1]  = "ETH_RMII_MDC"
        self.pins['C'][4]  = "ETH_RMII_RXD0"
        self.pins['C'][5]  = "ETH_RMII_RXD1"


    def remap_eth_rmii(self):
        if self.pins['D'][8] == "GPIO" and self.pins['D'][9] == "GPIO" \
           and self.pins['D'][10] == "GPIO":
            
            self.pins['D'][8] = self.pins['A'][7]
            self.pins['D'][9] = self.pins['C'][4]
            self.pins['D'][10] = self.pins['C'][5]

            self.pins['A'][7] = "GPIO"
            self.pins['C'][4] = "GPIO"
            self.pins['C'][5] = "GPIO"
            return True
        else:
            return False


    def set_sdio(self):
        if self.eth_mii_widget.checkState() == Qt.CheckState.Checked:
            raise Exception(f"Конфликт ETH MII и SDIO -> B8 = {self.pins['B'][8]}\n"
                            "Нельзя одновременно разместить ETH MII и SDIO")
        else:
            self.pins['B'][8]  = "SDIO_D4"
        self.pins['B'][9]  = "SDIO_D5"
        self.pins['C'][6]  = "SDIO_D6"
        self.pins['C'][7]  = "SDIO_D7"
        if self.eth_option_widget.checkState() == Qt.CheckState.Checked:
            self.pins['B'][14] = "SDIO_D0"
            self.pins['B'][15] = "SDIO_D1"
        else:
            self.pins['C'][8]  = "SDIO_D0"
            self.pins['C'][9]  = "SDIO_D1"
        self.pins['C'][10] = "SDIO_D2"
        self.pins['C'][11] = "SDIO_D3"
        self.pins['C'][12] = "SDIO_CK"
        if self.pins['D'][2] == "GPIO":
            self.pins['D'][2]  = "SDIO_CMD"
        else:
            raise Exception(f"Конфликт FSMC и SDIO -> D2 = {self.pins['D'][2]}\n"
                            "Нельзя одновременно разместить FSMC, SDIO и USB")


    def set_tim5(self):
        if self.eth_mii_widget.checkState() == Qt.CheckState.Checked:
            raise Exception(f"Конфликт ETH MII и TIM 5 -> A0 = {self.pins['A'][0]}\n"
                "Нельзя одновременно разместить ETH MII и TIM 5")
        elif self.eth_rgmii_widget.checkState() == Qt.CheckState.Checked:
            raise Exception(f"Конфликт ETH RGMII и TIM 5 -> A0 = {self.pins['A'][0]}\n"
                "Нельзя одновременно разместить ETH RGMII и TIM 5")
        elif self.eth_rmii_widget.checkState() == Qt.CheckState.Checked:
            raise Exception(f"Конфликт ETH RMII и TIM 5 -> A1 = {self.pins['A'][1]}\n"
                "Нельзя одновременно разместить ETH RMII и TIM 5")
        else:
            self.pins['A'][0] = "TIM5_CH1"
            self.pins['A'][1] = "TIM5_CH2"
            self.pins['A'][2] = "TIM5_CH3"
            self.pins['A'][3] = "TIM5_CH4"


    def set_eth(self):
        if self.dvp_widget.checkState() == Qt.CheckState.Checked:
            raise Exception(f"Конфликт DVP и ETH 10M PHY -> С8 = {self.pins['C'][8]}\n"
                "Нельзя одновременно разместить DVP и ETH 10M PHY")
        elif self.sdio_widget.checkState() == Qt.CheckState.Checked:
            raise Exception(f"Конфликт SDIO и ETH 10M PHY -> С6 = {self.pins['C'][6]}\n"
                "Нельзя одновременно разместить SDIO и ETH 10M PHY")
        else:
            self.pins['C'][6] = "ETH_RXP"
            self.pins['C'][7] = "ETH_RXN"
            self.pins['C'][8] = "ETH_TXP"
            self.pins['C'][9] = "ETH_TXN"


    def set_otg_fs(self):
        if self.dvp_widget.checkState() == Qt.CheckState.Checked:
            raise Exception(f"Конфликт DVP и OTG FS -> A9 = {self.pins['A'][9]}\n"
                "Нельзя одновременно разместить DVP и OTG FS")
        else:
            self.pins['A'][9]  = "OTG_FS_VBUS"
            self.pins['A'][10] = "OTG_FS_ID"
            self.pins['A'][11] = "OTG_FS_DM"
            self.pins['A'][12] = "OTG_FS_DP"


    def set_usbhs(self):
        self.pins['B'][6] = "USBHS_DM"
        self.pins['B'][7] = "USBHS_DP"


    def set_usbfs(self):
        self.pins['B'][6] = "USBFS_DM"
        self.pins['B'][7] = "USBFS_DP"


    def set_hse(self):
        if self.fsmc_widget.checkState() == Qt.CheckState.Checked:
            raise Exception(f"Конфликт FSMC и HSE -> D0 = {self.pins['D'][0]}\n"
                "Нельзя одновременно разместить FSMC и HSE")
        else:
            self.pins['D'][0] = "HSE_OSC_IN"
            self.pins['D'][1] = "HSE_OSC_OUT"


    def set_lse(self):
        self.pins['C'][14] = "LSE_OSC32_IN"
        self.pins['C'][15] = "LSE_OSC32_OUT"


    def set_tim9(self):
        if self.pins['A'][2] == "GPIO" and self.pins['A'][3] == "GPIO" and \
		   self.pins['A'][4] == "GPIO" and self.pins['C'][0] == "GPIO" and \
		   self.pins['C'][1] == "GPIO" and self.pins['C'][2] == "GPIO" and \
           self.pins['C'][4] == "GPIO" and self.pins['C'][5] == "GPIO":
            
            self.pins['A'][2] = "TIM9_CH1_ETR"
            self.pins['A'][3] = "TIM9_CH2"
            self.pins['A'][4] = "TIM9_CH3"
            self.pins['C'][0] = "TIM9_CH1N"
            self.pins['C'][1] = "TIM9_CH2N"
            self.pins['C'][2] = "TIM9_CH3N"
            self.pins['C'][4] = "TIM9_CH4"
            self.pins['C'][5] = "TIM9_BKIN"
        else:
            if not(self.remap1_tim9()):
                if not(self.remap2_tim9()):
                    raise Exception(f"Не удаётся разместить TIM 9")


    def remap1_tim9(self):
        if self.pins['A'][1] == "GPIO" and self.pins['A'][2] == "GPIO" and \
		   self.pins['A'][3] == "GPIO" and self.pins['A'][4] == "GPIO" and \
		   self.pins['B'][0] == "GPIO" and self.pins['B'][1] == "GPIO" and \
           self.pins['B'][2] == "GPIO" and self.pins['C'][14] == "GPIO":

            self.pins['A'][1]  = "TIM9_BKIN"
            self.pins['A'][2]  = "TIM9_CH1_ETR"
            self.pins['A'][3]  = "TIM9_CH2"
            self.pins['A'][4]  = "TIM9_CH3"
            self.pins['B'][0]  = "TIM9_CH1N"
            self.pins['B'][1]  = "TIM9_CH2N"
            self.pins['B'][2]  = "TIM9_CH3N"
            self.pins['C'][14] = "TIM9_CH4"
            return True
        else:
            return False


    def remap2_tim9(self):
        if self.pins['D'][8] == "GPIO" and self.pins['D'][9] == "GPIO" and \
		   self.pins['D'][10] == "GPIO" and self.pins['D'][11] == "GPIO" and \
		   self.pins['D'][12] == "GPIO" and self.pins['D'][13] == "GPIO" and \
           self.pins['D'][14] == "GPIO" and self.pins['D'][15] == "GPIO":

            self.pins['D'][8]  = "TIM9_CH1N"
            self.pins['D'][9]  = "TIM9_CH1_ETR"
            self.pins['D'][10] = "TIM9_CH2N"
            self.pins['D'][11] = "TIM9_CH2"
            self.pins['D'][12] = "TIM9_CH3N"
            self.pins['D'][13] = "TIM9_CH3"
            self.pins['D'][14] = "TIM9_BKIN"
            self.pins['D'][15] = "TIM9_CH4"
            return True
        else:
            return False


    def set_tim2(self):
        if self.pins['A'][0] == "GPIO" and self.pins['A'][1] == "GPIO" and \
		   self.pins['A'][2] == "GPIO" and self.pins['A'][3] == "GPIO":
            
            self.pins['A'][0] = "TIM2_CH1_ETR"
            self.pins['A'][1] = "TIM2_CH2"
            self.pins['A'][2] = "TIM2_CH3"
            self.pins['A'][3] = "TIM2_CH4"
        else:
            if not(self.remap1_tim2()):
                if not(self.remap2_tim2()):
                    if not(self.remap3_tim2()):
                        raise Exception(f"Не удаётся разместить TIM 2")


    def remap1_tim2(self):
        if self.pins['A'][2] == "GPIO" and self.pins['A'][3] == "GPIO" and \
		   self.pins['A'][15] == "GPIO" and self.pins['B'][3] == "GPIO":

            self.pins['A'][2]  = "TIM2_CH3"
            self.pins['A'][3]  = "TIM2_CH4"
            self.pins['A'][15] = "TIM2_CH1_ETR"
            self.pins['B'][3]  = "TIM2_CH2"
            return True
        else:
            return False


    def remap2_tim2(self):
        if self.pins['A'][0] == "GPIO" and self.pins['A'][1] == "GPIO" and \
		   self.pins['B'][10] == "GPIO" and self.pins['B'][11] == "GPIO":

            self.pins['A'][0]  = "TIM2_CH1_ETR"
            self.pins['A'][1]  = "TIM2_CH2"
            self.pins['B'][10] = "TIM2_CH3"
            self.pins['B'][11] = "TIM2_CH4"
            return True
        else:
            return False


    def remap3_tim2(self):
        if self.pins['A'][15] == "GPIO" and self.pins['B'][3] == "GPIO" and \
		   self.pins['B'][10] == "GPIO" and self.pins['B'][11] == "GPIO":

            self.pins['A'][15] = "TIM2_CH1_ETR"
            self.pins['B'][3]  = "TIM2_CH2"
            self.pins['B'][10] = "TIM2_CH3"
            self.pins['B'][11] = "TIM2_CH4"
            return True
        else:
            return False


    def set_dac(self, value):
        if value == 1:
            if self.pins['A'][4] == "GPIO":
                self.pins['A'][4] = "DAC_OUT1"
            else:
                if self.pins['A'][5] == "GPIO":
                    self.pins['A'][5] = "DAC_OUT2"
                else:
                    raise Exception(f"Не удаётся разместить DAC")
        elif value == 2:
            if self.pins['A'][4] == "GPIO" and self.pins['A'][5] == "GPIO":
                self.pins['A'][4] = "DAC_OUT1"
                self.pins['A'][5] = "DAC_OUT2"
            else:
                raise Exception("Не удаётся разместить DAC")


    def set_i2s(self, value):
        try:
            if value == 1:
                try:
                    self.set_i2s2()
                except:
                    self.set_i2s3()
            elif value == 2:
                self.set_i2s2()
                self.set_i2s3()
        except:
            raise Exception("Не удаётся разместить I2S")


    def set_i2s2(self):
        if self.pins['B'][12] == "GPIO" and self.pins['B'][13] == "GPIO" and \
		   self.pins['B'][15] == "GPIO" and self.pins['C'][6] == "GPIO":

            self.pins['B'][12] = "I2S2_WS"
            self.pins['B'][13] = "I2S2_CK"
            self.pins['B'][15] = "I2S2_SD"
            self.pins['C'][6]  = "I2S2_MCK"
        else:
            raise Exception("Не удаётся разместить I2S2")


    def set_i2s3(self):
        if self.pins['A'][15] == "GPIO" and self.pins['B'][3] == "GPIO" and \
		   self.pins['B'][5] == "GPIO" and self.pins['C'][7] == "GPIO":

            self.pins['A'][15] = "I2S3_WS"
            self.pins['B'][3]  = "I2S3_CK"
            self.pins['B'][5]  = "I2S3_SD"
            self.pins['C'][7]  = "I2S3_MCK"
        else:
            if not(self.remap_i2s3()):
                raise Exception("Не удаётся разместить I2S3")


    def remap_i2s3(self):
        if self.pins['A'][4] == "GPIO" and self.pins['C'][7] == "GPIO" and \
		   self.pins['C'][10] == "GPIO" and self.pins['C'][12] == "GPIO":
        
            self.pins['A'][4]  = "I2S3_WS"
            self.pins['C'][7]  = "I2S3_MCK"
            self.pins['C'][10] = "I2S3_CK"
            self.pins['C'][12] = "I2S3_SD"
            return True
        else:
            return False


    def set_i2c(self, value):
        try:
            if value == 1:
                try:
                    self.set_i2c1()
                except:
                    self.set_i2c2()
            elif value == 2:
                self.set_i2c1()
                self.set_i2c2()
        except:
            raise Exception("Не удаётся разместить I2C")


    def set_i2c1(self):
        if self.pins['B'][5] == "GPIO" and self.pins['B'][6] == "GPIO" and \
		   self.pins['B'][7] == "GPIO":

            self.pins['B'][5] = "I2C1_SMBA"
            self.pins['B'][6] = "I2C1_SCL"
            self.pins['B'][7] = "I2C1_SDA"
        else:
            if not(self.remap_i2c1()):
                raise Exception(f"Не удаётся разместить I2C1")


    def remap_i2c1(self):
        if self.pins['B'][5] == "GPIO" and self.pins['B'][8] == "GPIO" and \
		   self.pins['B'][9] == "GPIO":
        
            self.pins['B'][5] = "I2C1_SMBA"
            self.pins['B'][8] = "I2C1_SCL"
            self.pins['B'][9] = "I2C1_SDA"
            return True
        else:
            return False


    def set_i2c2(self):
        if self.pins['B'][10] == "GPIO" and self.pins['B'][11] == "GPIO" and \
		   self.pins['B'][12] == "GPIO":

            self.pins['B'][10] = "I2C2_SCL"
            self.pins['B'][11] = "I2C2_SDA"
            self.pins['B'][12] = "I2C2_SMBA"
        else:
            raise Exception(f"Не удаётся разместить I2C2")


    def set_tim_3_4(self, value):
        try:
            if value == 1:
                try:
                    self.set_tim3()
                except:
                    self.set_tim4()
            elif value == 2:
                self.set_tim3()
                self.set_tim4()
        except:
            raise Exception("Не удаётся разместить один из таймеров TIM 3 / TIM 4")


    def set_tim3(self):
        if self.pins['A'][7] == "ETH_RMII_CRS_DV":
            if not(self.remap_eth_rmii()):
                if not(self.remap1_tim3()):
                    if not(self.remap2_tim3()):
                        raise Exception(f"Не удаётся разместить TIM 3")
        
        if self.pins['B'][0] == "ETH_MII_RXD2":
            if not(self.remap_eth_mii()):
                if not(self.remap1_tim3()):
                    if not(self.remap2_tim3()):
                        raise Exception(f"Не удаётся разместить TIM 3")

        if self.pins['A'][6] == "GPIO" and self.pins['A'][7] == "GPIO" \
           and self.pins['B'][0] == "GPIO" and self.pins['B'][1] == "GPIO" \
           and self.pins['D'][2] == "GPIO":
        
            self.pins['A'][6] = "TIM3_CH1"
            self.pins['A'][7] = "TIM3_CH2"
            self.pins['B'][0] = "TIM3_CH3"
            self.pins['B'][1] = "TIM3_CH4"
            self.pins['D'][2] = "TIM3_ETR"
        else:
            if not(self.remap1_tim3()):
                if not(self.remap2_tim3()):
                    raise Exception(f"Не удаётся разместить TIM 3")


    def remap1_tim3(self):
        if self.pins['B'][0] == "GPIO" and self.pins['B'][1] == "GPIO" \
           and self.pins['B'][4] == "GPIO" and self.pins['B'][5] == "GPIO" \
           and self.pins['D'][2] == "GPIO":

            self.pins['B'][0] = "TIM3_CH3"
            self.pins['B'][1] = "TIM3_CH4"
            self.pins['B'][4] = "TIM3_CH1"
            self.pins['B'][5] = "TIM3_CH2"
            self.pins['D'][2] = "TIM3_ETR"
            return True
        else:
            return False


    def remap2_tim3(self):
        if self.pins['C'][6] == "GPIO" and self.pins['C'][7] == "GPIO" \
           and self.pins['C'][8] == "GPIO" and self.pins['C'][9] == "GPIO" \
           and self.pins['D'][2] == "GPIO":

            self.pins['C'][6] = "TIM3_CH1"
            self.pins['C'][7] = "TIM3_CH2"
            self.pins['C'][8] = "TIM3_CH3"
            self.pins['C'][9] = "TIM3_CH4"
            self.pins['D'][2] = "TIM3_ETR"
            return True
        else:
            return False


    def set_tim4(self):
        if self.pins['B'][6] == "GPIO" and self.pins['B'][7] == "GPIO" \
           and self.pins['B'][8] == "GPIO" and self.pins['B'][9] == "GPIO" \
           and self.pins['E'][0] == "GPIO":

            self.pins['B'][6] = "TIM4_CH1"
            self.pins['B'][7] = "TIM4_CH2"
            self.pins['B'][8] = "TIM4_CH3"
            self.pins['B'][9] = "TIM4_CH4"
            self.pins['E'][0] = "TIM4_ETR"
        else:
            if not(self.remap_tim4()):
                raise Exception(f"Не удаётся разместить TIM 4")


    def remap_tim4(self):
        if self.pins['D'][12] == "GPIO" and self.pins['D'][13] == "GPIO" \
           and self.pins['D'][14] == "GPIO" and self.pins['D'][15] == "GPIO" \
           and self.pins['E'][0] == "GPIO":

            self.pins['D'][12] = "TIM4_CH1"
            self.pins['D'][13] = "TIM4_CH2"
            self.pins['D'][14] = "TIM4_CH3"
            self.pins['D'][15] = "TIM4_CH4"
            self.pins['E'][0]  = "TIM4_ETR"
            return True
        else:
            return False


    def set_can(self, value):
        try:
            if value == 1:
                try:
                    self.set_can1()
                except:
                    self.set_can2()
            elif value == 2:
                self.set_can1()
                self.set_can2()
        except:
            raise Exception("Не удаётся разместить CAN")


    def set_can1(self):
        if self.pins['A'][11] == "GPIO" and self.pins['A'][12] == "GPIO":
            self.pins['A'][11] = "CAN1_RX"
            self.pins['A'][12] = "CAN1_TX"
        else:
            if not(self.remap1_can1()):
                if not(self.remap2_can1()):
                    raise Exception(f"Не удаётся разместить CAN 1")


    def remap1_can1(self):
        if self.pins['B'][8] == "GPIO" and self.pins['B'][9] == "GPIO":
            self.pins['B'][8] = "CAN1_RX"
            self.pins['B'][9] = "CAN1_TX"
            return True
        else:
            return False


    def remap2_can1(self):
        if self.pins['D'][0] == "GPIO" and self.pins['D'][1] == "GPIO":
            self.pins['D'][0] = "CAN1_RX"
            self.pins['D'][1] = "CAN1_TX"
            return True
        else:
            return False


    def set_can2(self):
        if self.pins['B'][5] == "GPIO" and self.pins['B'][6] == "GPIO":
            self.pins['B'][5] = "CAN2_RX"
            self.pins['B'][6] = "CAN2_TX"
        else:
            if not(self.remap_can2()):
                raise Exception(f"Не удаётся разместить CAN 2")


    def remap_can2(self):
        if self.pins['B'][12] == "GPIO" and self.pins['B'][13] == "GPIO":
            self.pins['B'][12] = "CAN2_RX"
            self.pins['B'][13] = "CAN2_TX"
            return True
        else:
            return False


    def set_spi(self, value):
        if value == 1:
            try:
                self.set_spi1()
            except:
                try:
                    self.set_spi2()
                except:
                    try:
                        self.set_spi3()
                    except:
                        raise Exception("Не удаётся разместить SPI")
        if value == 2:
            try:
                self.set_spi1()
                self.set_spi2()
            except Exception as exc:
                if str(exc) == "Не удаётся разместить SPI 1":
                    try:
                        self.set_spi2()
                        self.set_spi3()
                    except:
                        raise Exception("Не удаётся разместить SPI")
                if str(exc) == "Не удаётся разместить SPI 2":
                    try:
                        self.set_spi3()
                    except:
                        raise Exception("Не удаётся разместить SPI")
        if value == 3:
            try:
                self.set_spi1()
                self.set_spi2()
                self.set_spi3()
            except:
                raise Exception("Не удаётся разместить SPI")


    def set_spi1(self):
        if self.pins['A'][7] == "ETH_RMII_CRS_DV":
            if not(self.remap_eth_rmii()):
                if not(self.remap_spi1()):
                    raise Exception(f"Не удаётся разместить SPI 1")

        if self.pins['A'][4] == "GPIO" and self.pins['A'][5] == "GPIO" \
           and self.pins['A'][6] == "GPIO" and self.pins['A'][7] == "GPIO":
            
            self.pins['A'][4] = "SPI1_NSS"
            self.pins['A'][5] = "SPI1_SCK"
            self.pins['A'][6] = "SPI1_MISO"
            self.pins['A'][7] = "SPI1_MOSI"
        else:
            if not(self.remap_spi1()):
                raise Exception(f"Не удаётся разместить SPI 1")


    def remap_spi1(self):
        if self.pins['A'][15] == "GPIO" and self.pins['B'][3] == "GPIO" \
           and self.pins['B'][4] == "GPIO" and self.pins['B'][5] == "GPIO":

            self.pins['A'][15] = "SPI1_NSS"
            self.pins['B'][3]  = "SPI1_SCK"
            self.pins['B'][4]  = "SPI1_MISO"
            self.pins['B'][5]  = "SPI1_MOSI"
            return True
        else:
            return False


    def set_spi2(self):
        if self.pins['B'][12] == "GPIO" and self.pins['B'][13] == "GPIO" \
           and self.pins['B'][14] == "GPIO" and self.pins['B'][15] == "GPIO":

            self.pins['B'][12] = "SPI2_NSS"
            self.pins['B'][13] = "SPI2_SCK"
            self.pins['B'][14] = "SPI2_MISO"
            self.pins['B'][15] = "SPI2_MOSI"
        else:
            raise Exception(f"Не удаётся разместить SPI 2")


    def set_spi3(self):
        if self.pins['A'][15] == "GPIO" and self.pins['B'][3] == "GPIO" \
           and self.pins['B'][4] == "GPIO" and self.pins['B'][5] == "GPIO":

            self.pins['A'][15] = "SPI3_NSS"
            self.pins['B'][3]  = "SPI3_SCK"
            self.pins['B'][4]  = "SPI3_MISO"
            self.pins['B'][5]  = "SPI3_MOSI"
        else:
            if not(self.remap_spi3()):
                raise Exception(f"Не удаётся разместить SPI 3")


    def remap_spi3(self):
        if self.pins['A'][4] == "GPIO" and self.pins['C'][10] == "GPIO" \
           and self.pins['C'][11] == "GPIO" and self.pins['C'][12] == "GPIO":

            self.pins['A'][4]  = "SPI3_NSS"
            self.pins['C'][10] = "SPI3_SCK"
            self.pins['C'][11] = "SPI3_MISO"
            self.pins['C'][12] = "SPI3_MOSI"
            return True
        else:
            return False


    def set_tim_1_8_10(self, value):
        if value == 1:
            try:
                self.set_tim1()
            except:
                try:
                    self.set_tim8()
                except:
                    try:
                        self.set_tim10()
                    except:
                        raise Exception("Не удаётся разместить один из таймеров TIM 1 / TIM 8 / TIM 10")
        if value == 2:
            try:
                self.set_tim1()
                self.set_tim8()
            except Exception as exc:
                if str(exc) == "Не удаётся разместить TIM 1":
                    try:
                        self.set_tim8()
                        self.set_tim10()
                    except:
                        raise Exception("Не удаётся разместить один из таймеров TIM 1 / TIM 8 / TIM 10")
                if str(exc) == "Не удаётся разместить TIM 8":
                    try:
                        self.set_tim10()
                    except:
                        raise Exception("Не удаётся разместить один из таймеров TIM 1 / TIM 8 / TIM 10")
        if value == 3:
            try:
                self.set_tim1()
                self.set_tim8()
                self.set_tim10()
            except:
                raise Exception("Не удаётся разместить один из таймеров TIM 1 / TIM 8 / TIM 10")


    def set_tim1(self):
        if self.pins['A'][8] == "GPIO" and self.pins['A'][9] == "GPIO" and \
		   self.pins['A'][10] == "GPIO" and self.pins['A'][11] == "GPIO" and \
		   self.pins['A'][12] == "GPIO" and self.pins['B'][12] == "GPIO" and \
           self.pins['B'][13] == "GPIO" and self.pins['B'][14] == "GPIO" and \
           self.pins['B'][15] == "GPIO":

            self.pins['A'][8]  = "TIM1_CH1"
            self.pins['A'][9]  = "TIM1_CH2"
            self.pins['A'][10] = "TIM1_CH3"
            self.pins['A'][11] = "TIM1_CH4"
            self.pins['A'][12] = "TIM1_ETR"
            self.pins['B'][12] = "TIM1_BKIN"
            self.pins['B'][13] = "TIM1_CH1N"
            self.pins['B'][14] = "TIM1_CH2N"
            self.pins['B'][15] = "TIM1_CH3N"
        else:
            if not(self.remap1_tim1()):
                if not(self.remap2_tim1()):
                    raise Exception(f"Не удаётся разместить TIM 1")


    def remap1_tim1(self):
        if self.pins['A'][7] == "ETH_RMII_CRS_DV":
            if not(self.remap_eth_rmii()):
                return False

        if self.pins['B'][0] == "ETH_MII_RXD2":
            if not(self.remap_eth_mii()):
                return False

        if self.pins['A'][6] == "GPIO" and self.pins['A'][7] == "GPIO" and \
		   self.pins['A'][8] == "GPIO" and self.pins['A'][9] == "GPIO" and \
		   self.pins['A'][10] == "GPIO" and self.pins['A'][11] == "GPIO" and \
           self.pins['A'][12] == "GPIO" and self.pins['B'][0] == "GPIO" and \
           self.pins['B'][1] == "GPIO":

            self.pins['A'][6]  = "TIM1_BKIN"
            self.pins['A'][7]  = "TIM1_CH1N"
            self.pins['A'][8]  = "TIM1_CH1"
            self.pins['A'][9]  = "TIM1_CH2"
            self.pins['A'][10] = "TIM1_CH3"
            self.pins['A'][11] = "TIM1_CH4"
            self.pins['A'][12] = "TIM1_ETR"
            self.pins['B'][0]  = "TIM1_CH2N"
            self.pins['B'][1]  = "TIM1_CH3N"
            return True
        else:
            return False


    def remap2_tim1(self):
        if self.pins['E'][7] == "GPIO" and self.pins['E'][8] == "GPIO" and \
		   self.pins['E'][9] == "GPIO" and self.pins['E'][10] == "GPIO" and \
		   self.pins['E'][11] == "GPIO" and self.pins['E'][12] == "GPIO" and \
           self.pins['E'][13] == "GPIO" and self.pins['E'][14] == "GPIO" and \
           self.pins['E'][15] == "GPIO":

            self.pins['E'][7]  = "TIM1_ETR"
            self.pins['E'][8]  = "TIM1_CH1N"
            self.pins['E'][9]  = "TIM1_CH1"
            self.pins['E'][10] = "TIM1_CH2N"
            self.pins['E'][11] = "TIM1_CH2"
            self.pins['E'][12] = "TIM1_CH3N"
            self.pins['E'][13] = "TIM1_CH3"
            self.pins['E'][14] = "TIM1_CH4"
            self.pins['E'][15] = "TIM1_BKIN"
            return True
        else:
            return False


    def set_tim8(self):
        if self.pins['A'][7] == "ETH_RMII_CRS_DV":
            if not(self.remap_eth_rmii()):
                if not(self.remap_tim8()):
                    raise Exception(f"Не удаётся разместить TIM 8")

        if self.pins['A'][0] == "GPIO" and self.pins['A'][6] == "GPIO" \
           and self.pins['A'][7] == "GPIO" and self.pins['B'][0] == "GPIO" \
           and self.pins['B'][1] == "GPIO" and self.pins['C'][6] == "GPIO" \
           and self.pins['C'][7] == "GPIO" and self.pins['C'][8] == "GPIO" \
           and self.pins['C'][9] == "GPIO":
            
            self.pins['A'][0] = "TIM8_ETR"
            self.pins['A'][6] = "TIM8_BKIN"
            self.pins['A'][7] = "TIM8_CH1N"
            self.pins['B'][0] = "TIM8_CH2N"
            self.pins['B'][1] = "TIM8_CH3N"
            self.pins['C'][6] = "TIM8_CH1"
            self.pins['C'][7] = "TIM8_CH2"
            self.pins['C'][8] = "TIM8_CH3"
            self.pins['C'][9] = "TIM8_CH4"
        else:
            if not(self.remap_tim8()):
                raise Exception(f"Не удаётся разместить TIM 8")


    def remap_tim8(self):
        if self.pins['A'][0] == "GPIO" and self.pins['A'][13] == "GPIO" \
           and self.pins['A'][14] == "GPIO" and self.pins['A'][15] == "GPIO" \
           and self.pins['B'][6] == "GPIO" and self.pins['B'][7] == "GPIO" \
           and self.pins['B'][8] == "GPIO" and self.pins['B'][9] == "GPIO" \
           and self.pins['C'][13] == "GPIO":

            self.pins['A'][0]  = "TIM8_ETR"
            self.pins['A'][13] = "TIM8_CH1N"
            self.pins['A'][14] = "TIM8_CH2N"
            self.pins['A'][15] = "TIM8_CH3N"
            self.pins['B'][6]  = "TIM8_CH1"
            self.pins['B'][7]  = "TIM8_CH2"
            self.pins['B'][8]  = "TIM8_CH3"
            self.pins['B'][9]  = "TIM8_BKIN"
            self.pins['C'][13] = "TIM8_CH4"
            return True
        else:
            return False


    def set_tim10(self):
        if self.pins['A'][12] == "GPIO" and self.pins['A'][13] == "GPIO" \
           and self.pins['A'][14] == "GPIO" and self.pins['B'][8] == "GPIO" \
           and self.pins['B'][9] == "GPIO" and self.pins['C'][3] == "GPIO" \
           and self.pins['C'][10] == "GPIO" and self.pins['C'][11] == "GPIO" \
           and self.pins['C'][12] == "GPIO":

            self.pins['A'][12] = "TIM10_CH1N"
            self.pins['A'][13] = "TIM10_CH2N"
            self.pins['A'][14] = "TIM10_CH3N"
            self.pins['B'][8]  = "TIM10_CH1"
            self.pins['B'][9]  = "TIM10_CH2"
            self.pins['C'][3]  = "TIM10_CH3"
            self.pins['C'][10] = "TIM10_ETR"
            self.pins['C'][11] = "TIM10_CH4"
            self.pins['C'][12] = "TIM10_BKIN"
        else:
            if not(self.remap1_tim10()):
                if not(self.remap2_tim10()):
                    raise Exception(f"Не удаётся разместить TIM 10")


    def remap1_tim10(self):
        if self.pins['A'][5] == "GPIO" and self.pins['A'][6] == "GPIO" \
           and self.pins['A'][7] == "GPIO" and self.pins['B'][3] == "GPIO" \
           and self.pins['B'][4] == "GPIO" and self.pins['B'][5] == "GPIO" \
           and self.pins['B'][10] == "GPIO" and self.pins['B'][11] == "GPIO" \
           and self.pins['C'][15] == "GPIO":

            self.pins['A'][5]  = "TIM10_CH1N"
            self.pins['A'][6]  = "TIM10_CH2N"
            self.pins['A'][7]  = "TIM10_CH3N"
            self.pins['B'][3]  = "TIM10_CH1"
            self.pins['B'][4]  = "TIM10_CH2"
            self.pins['B'][5]  = "TIM10_CH3"
            self.pins['B'][10] = "TIM10_BKIN"
            self.pins['B'][11] = "TIM10_ETR"
            self.pins['C'][15] = "TIM10_CH4"
            return True
        else:
            return False


    def remap2_tim10(self):
        if self.pins['D'][0] == "GPIO" and self.pins['D'][1] == "GPIO" \
           and self.pins['D'][3] == "GPIO" and self.pins['D'][5] == "GPIO" \
           and self.pins['D'][7] == "GPIO" and self.pins['E'][2] == "GPIO" \
           and self.pins['E'][3] == "GPIO" and self.pins['E'][4] == "GPIO" \
           and self.pins['E'][5] == "GPIO":

            self.pins['D'][0] = "TIM10_ETR"
            self.pins['D'][1] = "TIM10_CH1"
            self.pins['D'][3] = "TIM10_CH2"
            self.pins['D'][5] = "TIM10_CH3"
            self.pins['D'][7] = "TIM10_CH4"
            self.pins['E'][2] = "TIM10_BKIN"
            self.pins['E'][3] = "TIM10_CH1N"
            self.pins['E'][4] = "TIM10_CH2N"
            self.pins['E'][5] = "TIM10_CH3N"
            return True
        else:
            return False


    def set_opa(self, value):
        if value == 1:
            try:
                self.set_opa1()
            except:
                try:
                    self.set_opa2()
                except:
                    try:
                        self.set_opa3()
                    except:
                        try:
                            self.set_opa4()
                        except:
                            raise Exception("Не удаётся разместить OPA")
        if value == 2:
            try:
                self.set_opa1()
                self.set_opa2()
            except Exception as exc:
                if str(exc) == "Не удаётся разместить OPA 1":
                    try:
                        self.set_opa2()
                        self.set_opa3()
                    except Exception as exc2:
                        if str(exc2) == "Не удаётся разместить OPA 2":
                            try:
                                self.set_opa3()
                                self.set_opa4()
                            except:
                                raise Exception("Не удаётся разместить OPA")
                        if str(exc2) == "Не удаётся разместить OPA 3":
                            try:
                                self.set_opa4()
                            except:
                                raise Exception("Не удаётся разместить OPA")
                if str(exc) == "Не удаётся разместить OPA 2":
                    try:
                        self.set_opa3()
                    except:
                        try:
                            self.set_opa4()
                        except:
                            raise Exception("Не удаётся разместить OPA")
        if value == 3:
            try:
                self.set_opa1()
                self.set_opa2()
                self.set_opa3()
            except Exception as exc:
                if str(exc) == "Не удаётся разместить OPA 1":
                    try:
                        self.set_opa2()
                        self.set_opa3()
                        self.set_opa4()
                    except:
                        raise Exception("Не удаётся разместить OPA")
                if str(exc) == "Не удаётся разместить OPA 2":
                    try:
                        self.set_opa3()
                        self.set_opa4()
                    except:
                        raise Exception("Не удаётся разместить OPA")
                if str(exc) == "Не удаётся разместить OPA 3":
                    try:
                        self.set_opa4()
                    except:
                        raise Exception("Не удаётся разместить OPA")
        if value == 4:
            try:
                self.set_opa1()
                self.set_opa2()
                self.set_opa3()
                self.set_opa4()
            except:
                raise Exception("Не удаётся разместить OPA")


    def set_opa1(self):
        if self.pins['A'][3] == "GPIO" and self.pins['A'][6] == "GPIO" \
           and self.pins['B'][0] == "GPIO" and self.pins['B'][11] == "GPIO" \
           and self.pins['B'][15] == "GPIO" and self.pins['E'][15] == "GPIO":

            self.pins['A'][3]  = "OPA1_OUT0"
            self.pins['A'][6]  = "OPA1_CH1N"
            self.pins['B'][0]  = "OPA1_CH1P"
            self.pins['B'][11] = "OPA1_CH0N"
            self.pins['B'][15] = "OPA1_CH0P"
            self.pins['E'][15] = "OPA1_OUT1"
        else:
            raise Exception("Не удаётся разместить OPA 1")


    def set_opa2(self):
        if self.pins['A'][2] == "GPIO" and self.pins['A'][5] == "GPIO" \
           and self.pins['A'][7] == "GPIO" and self.pins['B'][10] == "GPIO" \
           and self.pins['B'][14] == "GPIO" and self.pins['E'][14] == "GPIO":

            self.pins['A'][2]  = "OPA2_OUT0"
            self.pins['A'][5]  = "OPA2_CH1N"
            self.pins['A'][7]  = "OPA2_CH1P"
            self.pins['B'][10] = "OPA2_CH0N"
            self.pins['B'][14] = "OPA2_CH0P"
            self.pins['E'][14] = "OPA2_OUT1"
        else:
            raise Exception("Не удаётся разместить OPA 2")


    def set_opa3(self):
        if self.pins['A'][1] == "GPIO" and self.pins['B'][2] == "GPIO" \
           and self.pins['B'][13] == "GPIO" and self.pins['C'][2] == "GPIO" \
           and self.pins['C'][5] == "GPIO" and self.pins['E'][7] == "GPIO":

            self.pins['A'][1]  = "OPA3_OUT0"
            self.pins['B'][2]  = "OPA3_CH0N"
            self.pins['B'][13] = "OPA3_CH0P"
            self.pins['C'][2]  = "OPA3_CH1N"
            self.pins['C'][5]  = "OPA3_CH1P"
            self.pins['E'][7]  = "OPA3_OUT1"
        else:
            raise Exception("Не удаётся разместить OPA 3")


    def set_opa4(self):
        if self.pins['A'][0] == "GPIO" and self.pins['B'][1] == "GPIO" \
           and self.pins['B'][12] == "GPIO" and self.pins['C'][3] == "GPIO" \
           and self.pins['C'][4] == "GPIO" and self.pins['E'][8] == "GPIO":

            self.pins['A'][0]  = "OPA4_OUT0"
            self.pins['B'][1]  = "OPA4_CH0N"
            self.pins['B'][12] = "OPA4_CH0P"
            self.pins['C'][3]  = "OPA4_CH1N"
            self.pins['C'][4]  = "OPA4_CH1P"
            self.pins['E'][8]  = "OPA4_OUT1"
        else:
            raise Exception("Не удаётся разместить OPA 4")


    def set_usart(self, value):
        if value == 1:
            try:
                self.set_usart1()
            except:
                try:
                    self.set_usart2()
                except:
                    try:
                        self.set_usart3()
                    except:
                        raise Exception("Не удаётся разместить USART")
        if value == 2:
            try:
                self.set_usart1()
                self.set_usart2()
            except Exception as exc:
                if str(exc) == "Не удаётся разместить USART 1":
                    try:
                        self.set_usart2()
                        self.set_usart3()
                    except:
                        raise Exception("Не удаётся разместить USART")
                if str(exc) == "Не удаётся разместить USART 2":
                    try:
                        self.set_usart3()
                    except:
                        raise Exception("Не удаётся разместить USART")
        if value == 3:
            try:
                self.set_usart1()
                self.set_usart2()
                self.set_usart3()
            except:
                raise Exception("Не удаётся разместить USART")


    def set_usart1(self):
        if self.check_usart1():
            raise Exception(f"Не удаётся разместить USART 1")
        else:
            if self.pins['A'][8] == "GPIO" and self.pins['A'][9] == "GPIO" and \
            self.pins['A'][10] == "GPIO" and self.pins['A'][11] == "GPIO" and \
            self.pins['A'][12] == "GPIO":

                self.pins['A'][8]  = "USART1_CK"
                self.pins['A'][9]  = "USART1_TX"
                self.pins['A'][10] = "USART1_RX"
                self.pins['A'][11] = "USART1_CTS"
                self.pins['A'][12] = "USART1_RTS"
            else:
                if not(self.remap1_usart1()):
                    if not(self.remap2_usart1()):
                        if not(self.remap3_usart1()):
                            raise Exception(f"Не удаётся разместить USART 1")


    def check_usart1(self):
        return (self.pins['A'][8] == "USART1_CK" and self.pins['A'][9] == "USART1_TX" and \
                self.pins['A'][10] == "USART1_RX" and self.pins['A'][11] == "USART1_CTS" and \
                self.pins['A'][12] == "USART1_RTS") or (self.pins['A'][8] == "USART1_CK" and \
                self.pins['A'][11] == "USART1_CTS" and self.pins['A'][12] == "USART1_RTS" and \
                self.pins['B'][6] == "USART1_TX" and self.pins['B'][7] == "USART1_RX") or \
               (self.pins['A'][5] == "USART1_CTS" and self.pins['A'][8] == "USART1_RX" and \
                self.pins['A'][9] == "USART1_RTS" and self.pins['A'][10] == "USART1_CK" and \
                self.pins['B'][15] == "USART1_TX") or (self.pins['A'][5] == "USART1_CK" and \
                self.pins['A'][6] == "USART1_TX" and self.pins['A'][7] == "USART1_RX" and \
                self.pins['C'][4] == "USART1_CTS" and self.pins['C'][5] == "USART1_RTS")


    def remap1_usart1(self):
        if self.pins['A'][8] == "GPIO" and self.pins['A'][11] == "GPIO" and \
		   self.pins['A'][12] == "GPIO" and self.pins['B'][6] == "GPIO" and \
		   self.pins['B'][7] == "GPIO":

            self.pins['A'][8]  = "USART1_CK"
            self.pins['A'][11] = "USART1_CTS"
            self.pins['A'][12] = "USART1_RTS"
            self.pins['B'][6]  = "USART1_TX"
            self.pins['B'][7]  = "USART1_RX"
            return True
        else:
            return False


    def remap2_usart1(self):
        if self.pins['A'][5] == "GPIO" and self.pins['A'][8] == "GPIO" and \
		   self.pins['A'][9] == "GPIO" and self.pins['A'][10] == "GPIO" and \
		   self.pins['B'][15] == "GPIO":

            self.pins['A'][5]  = "USART1_CTS"
            self.pins['A'][8]  = "USART1_RX"
            self.pins['A'][9]  = "USART1_RTS"
            self.pins['A'][10] = "USART1_CK"
            self.pins['B'][15] = "USART1_TX"
            return True
        else:
            return False


    def remap3_usart1(self):
        if self.pins['A'][7] == "ETH_RMII_CRS_DV":
            if not(self.remap_eth_rmii()):
                return False

        if self.pins['A'][7] == "ETH_MII_RX_DV":
            if not(self.remap_eth_mii()):
                return False

        if self.pins['A'][5] == "GPIO" and self.pins['A'][6] == "GPIO" and \
		   self.pins['A'][7] == "GPIO" and self.pins['C'][4] == "GPIO" and \
		   self.pins['C'][5] == "GPIO":

            self.pins['A'][5] = "USART1_CK"
            self.pins['A'][6] = "USART1_TX"
            self.pins['A'][7] = "USART1_RX"
            self.pins['C'][4] = "USART1_CTS"
            self.pins['C'][5] = "USART1_RTS"
            return True
        else:
            return False


    def set_usart2(self):
        if self.check_usart2():
            raise Exception(f"Не удаётся разместить USART 2")
        else:
            if self.pins['A'][0] == "GPIO" and self.pins['A'][1] == "GPIO" and \
            self.pins['A'][2] == "GPIO" and self.pins['A'][3] == "GPIO" and \
            self.pins['A'][4] == "GPIO":

                self.pins['A'][0] = "USART2_CTS"
                self.pins['A'][1] = "USART2_RTS"
                self.pins['A'][2] = "USART2_TX"
                self.pins['A'][3] = "USART2_RX"
                self.pins['A'][4] = "USART2_CK"
            else:
                if not(self.remap_usart2()):
                    raise Exception(f"Не удаётся разместить USART 2")


    def check_usart2(self):
        return (self.pins['A'][0] == "USART2_CTS" and self.pins['A'][1] == "USART2_RTS" and \
                self.pins['A'][2] == "USART2_TX" and self.pins['A'][3] == "USART2_RX" and \
                self.pins['A'][4] == "USART2_CK") or (self.pins['D'][3] == "USART2_CTS" and \
                self.pins['D'][4] == "USART2_RTS" and self.pins['D'][5] == "USART2_TX" and \
                self.pins['D'][6] == "USART2_RX" and self.pins['D'][7] == "USART2_CK")


    def remap_usart2(self):
        if self.pins['D'][3] == "GPIO" and self.pins['D'][4] == "GPIO" and \
		   self.pins['D'][5] == "GPIO" and self.pins['D'][6] == "GPIO" and \
		   self.pins['D'][7] == "GPIO":

            self.pins['D'][3] = "USART2_CTS"
            self.pins['D'][4] = "USART2_RTS"
            self.pins['D'][5] = "USART2_TX"
            self.pins['D'][6] = "USART2_RX"
            self.pins['D'][7] = "USART2_CK"
            return True
        else:
            return False


    def set_usart3(self):
        if self.check_usart3():
            raise Exception(f"Не удаётся разместить USART 3")
        else:
            if self.pins['B'][10] == "GPIO" and self.pins['B'][11] == "GPIO" and \
            self.pins['B'][12] == "GPIO" and self.pins['B'][13] == "GPIO" and \
            self.pins['B'][14] == "GPIO":

                self.pins['B'][10] = "USART3_TX"
                self.pins['B'][11] = "USART3_RX"
                self.pins['B'][12] = "USART3_CK"
                self.pins['B'][13] = "USART3_CTS"
                self.pins['B'][14] = "USART3_RTS"
            else:
                if not(self.remap1_usart3()):
                    if not(self.remap2_usart3()):
                        if not(self.remap3_usart3()):
                            raise Exception(f"Не удаётся разместить USART 3")


    def check_usart3(self):
        return (self.pins['B'][10] == "USART3_TX" and self.pins['B'][11] == "USART3_RX" and \
                self.pins['B'][12] == "USART3_CK" and self.pins['B'][13] == "USART3_CTS" and \
                self.pins['B'][14] == "USART3_RTS") or (self.pins['B'][13] == "USART3_CTS" and \
                self.pins['B'][14] == "USART3_RTS" and self.pins['C'][10] == "USART3_TX" and \
                self.pins['C'][11] == "USART3_RX" and self.pins['C'][12] == "USART3_CK") or \
               (self.pins['A'][13] == "USART3_TX" and self.pins['A'][14] == "USART3_RX" and \
                self.pins['D'][10] == "USART3_CK" and self.pins['D'][11] == "USART3_CTS" and \
                self.pins['D'][12] == "USART3_RTS") or (self.pins['D'][8] == "USART3_TX" and \
                self.pins['D'][9] == "USART3_RX" and self.pins['D'][10] == "USART3_CK" and \
                self.pins['D'][11] == "USART3_CTS" and self.pins['D'][12] == "USART3_RTS")


    def remap1_usart3(self):
        if self.pins['B'][13] == "GPIO" and self.pins['B'][14] == "GPIO" and \
		   self.pins['C'][10] == "GPIO" and self.pins['C'][11] == "GPIO" and \
		   self.pins['C'][12] == "GPIO":

            self.pins['B'][13] = "USART3_CTS"
            self.pins['B'][14] = "USART3_RTS"
            self.pins['C'][10] = "USART3_TX"
            self.pins['C'][11] = "USART3_RX"
            self.pins['C'][12] = "USART3_CK"
            return True
        else:
            return False


    def remap2_usart3(self):
        if self.pins['A'][13] == "GPIO" and self.pins['A'][14] == "GPIO" and \
		   self.pins['D'][10] == "GPIO" and self.pins['D'][11] == "GPIO" and \
		   self.pins['D'][12] == "GPIO":

            self.pins['A'][13] = "USART3_TX"
            self.pins['A'][14] = "USART3_RX"
            self.pins['D'][10] = "USART3_CK"
            self.pins['D'][11] = "USART3_CTS"
            self.pins['D'][12] = "USART3_RTS"
            return True
        else:
            return False


    def remap3_usart3(self):
        if self.pins['D'][8] == "GPIO" and self.pins['D'][9] == "GPIO" and \
		   self.pins['D'][10] == "GPIO" and self.pins['D'][11] == "GPIO" and \
		   self.pins['D'][12] == "GPIO":

            self.pins['D'][8]  = "USART3_TX"
            self.pins['D'][9]  = "USART3_RX"
            self.pins['D'][10] = "USART3_CK"
            self.pins['D'][11] = "USART3_CTS"
            self.pins['D'][12] = "USART3_RTS"
            return True
        else:
            return False


    def set_uart(self, value):
        usart = self.usart_widget.value()
        if value == 1:
            self.set_1_uart(usart)
        if value == 2:
            self.set_2_uarts(usart)
        if value == 3:
            self.set_3_uarts(usart)
        if value == 4:
            self.set_4_uarts(usart)
        if value == 5:
            self.set_5_uarts(usart)
        if value == 6:
            self.set_6_uarts(usart)
        if value == 7:
            self.set_7_uarts(usart)
        if value == 8:
            self.set_8_uarts()


    def set_1_uart(self, usart):
        try:
            self.set_uart4()
        except:
            try:
                self.set_uart5()
            except:
                self.u_map_6_7_8_1_2_3(usart)


    def set_2_uarts(self, usart):
        try:
            self.set_uart4()
            self.set_uart5()
        except Exception as exc:
            if str(exc) == "Не удаётся разместить UART 4":
                try:
                    self.set_uart5()
                    self.set_uart6()
                except Exception as exc2:
                    if str(exc2) == "Не удаётся разместить UART 5":
                        self.u_map_67_78_81_12_23_3_2_3(usart)

                    if str(exc2) == "Не удаётся разместить UART 6":
                        self.u_map_7_8_1_2_3(usart)

            if str(exc) == "Не удаётся разместить UART 5":
                self.u_map_6_7_8_1_2_3(usart)


    def set_3_uarts(self, usart):
        try:
            self.set_uart4()
            self.set_uart5()
            self.set_uart6()
        except Exception as exc:
            if str(exc) == "Не удаётся разместить UART 4":
                try:
                    self.set_uart5()
                    self.set_uart6()
                    self.set_uart7()
                except Exception as exc2:
                    if str(exc2) == "Не удаётся разместить UART 5":
                        self.u_map_678_781_812_123_23_3(usart)

                    if str(exc2) == "Не удаётся разместить UART 6":
                        self.u_map_78_81_12_23_3_2_3(usart)

                    if str(exc2) == "Не удаётся разместить UART 7":
                        self.u_map_8_1_2_3(usart)

            if str(exc) == "Не удаётся разместить UART 5":
                self.u_map_67_78_81_12_23_3_2_3(usart)

            if str(exc) == "Не удаётся разместить UART 6":
                self.u_map_7_8_1_2_3(usart)


    def set_4_uarts(self, usart):
        try:
            self.set_uart4()
            self.set_uart5()
            self.set_uart6()
            self.set_uart7()
        except Exception as exc:
            if str(exc) == "Не удаётся разместить UART 4":
                try:
                    self.set_uart5()
                    self.set_uart6()
                    self.set_uart7()
                    self.set_uart8()
                except Exception as exc2:
                    if str(exc2) == "Не удаётся разместить UART 5":
                        self.u_map_6781_7812_8123_123_23_3(usart)

                    if str(exc2) == "Не удаётся разместить UART 6":
                        self.u_map_781_812_123_23_3(usart)

                    if str(exc2) == "Не удаётся разместить UART 7":
                        self.u_map_81_12_23_3_2_3(usart)

                    if str(exc2) == "Не удаётся разместить UART 8":
                        self.u_map_1_2_3(usart)

            if str(exc) == "Не удаётся разместить UART 5":
                self.u_map_678_781_812_123_23_3(usart)

            if str(exc) == "Не удаётся разместить UART 6":
                self.u_map_78_81_12_23_3_2_3(usart)

            if str(exc) == "Не удаётся разместить UART 7":
                self.u_map_8_1_2_3(usart)


    def set_5_uarts(self, usart):
        try:
            self.set_uart4()
            self.set_uart5()
            self.set_uart6()
            self.set_uart7()
            self.set_uart8()
        except Exception as exc:
            if str(exc) == "Не удаётся разместить UART 4":
                if usart < 3:
                    try:
                        self.set_uart5()
                        self.set_uart6()
                        self.set_uart7()
                        self.set_uart8()
                        self.set_usart1()
                    except Exception as exc2:
                        if str(exc2) == "Не удаётся разместить UART 5":
                            if usart < 2:
                                try:
                                    self.set_uart6()
                                    self.set_uart7()
                                    self.set_uart8()
                                    self.set_usart1()
                                    self.set_usart2()
                                except Exception as exc3:
                                    if str(exc3) == "Не удаётся разместить UART 6":
                                        self.u_map_78123(usart)

                                    if str(exc3) == "Не удаётся разместить UART 7":
                                        self.u_map_8123(usart)

                                    if str(exc3) == "Не удаётся разместить UART 8":
                                        self.u_map_123(usart)

                                    if str(exc3) == "Не удаётся разместить USART 1":
                                        self.u_map_23(usart)

                                    if str(exc3) == "Не удаётся разместить USART 2":
                                        self.u_map_3(usart)
                            else:
                                raise Exception("Не удаётся разместить UART")

                        if str(exc2) == "Не удаётся разместить UART 6":
                            self.u_map_7812_8123_123_23_3(usart)

                        if str(exc2) == "Не удаётся разместить UART 7":
                            self.u_map_812_123_23_3(usart)

                        if str(exc2) == "Не удаётся разместить UART 8":
                            self.u_map_12_23_3(usart)

                        if str(exc2) == "Не удаётся разместить USART 1":
                            self.u_map_2_3(usart)
                else:
                    raise Exception("Не удаётся разместить UART")

            if str(exc) == "Не удаётся разместить UART 5":
                self.u_map_6781_7812_8123_123_23_3(usart)

            if str(exc) == "Не удаётся разместить UART 6":
                self.u_map_781_812_123_23_3(usart)

            if str(exc) == "Не удаётся разместить UART 7":
                self.u_map_81_12_23_3_2_3(usart)

            if str(exc) == "Не удаётся разместить UART 8":
                self.u_map_1_2_3(usart)


    def set_6_uarts(self, usart):
        try:
            self.set_uart4()
            self.set_uart5()
            self.set_uart6()
            self.set_uart7()
            self.set_uart8()
            self.set_usart1()
        except Exception as exc:
            if str(exc) == "Не удаётся разместить UART 4":
                if usart < 2:
                    try:
                        self.set_uart5()
                        self.set_uart6()
                        self.set_uart7()
                        self.set_uart8()
                        self.set_usart1()
                        self.set_usart2()
                    except Exception as exc2:
                        if str(exc2) == "Не удаётся разместить UART 5":
                            self.u_map_678123(usart)

                        if str(exc2) == "Не удаётся разместить UART 6":
                            self.u_map_78123(usart)

                        if str(exc2) == "Не удаётся разместить UART 7":
                            self.u_map_8123(usart)

                        if str(exc2) == "Не удаётся разместить UART 8":
                            self.u_map_123(usart)

                        if str(exc2) == "Не удаётся разместить USART 1":
                            self.u_map_23()

                        if str(exc2) == "Не удаётся разместить USART 2":
                            self.u_map_3()
                else:
                    raise Exception("Не удаётся разместить UART")

            if str(exc) == "Не удаётся разместить UART 5":
                if usart < 2:
                    try:
                        self.set_uart6()
                        self.set_uart7()
                        self.set_uart8()
                        self.set_usart1()
                        self.set_usart2()
                    except Exception as exc2:
                        if str(exc2) == "Не удаётся разместить UART 6":
                            self.u_map_78123(usart)

                        if str(exc2) == "Не удаётся разместить UART 7":
                            self.u_map_8123(usart)

                        if str(exc2) == "Не удаётся разместить UART 8":
                            self.u_map_123(usart)

                        if str(exc2) == "Не удаётся разместить USART 1":
                            self.u_map_23()

                        if str(exc2) == "Не удаётся разместить USART 2":
                            self.u_map_3()
                else:
                    raise Exception("Не удаётся разместить UART")

            if str(exc) == "Не удаётся разместить UART 6":
                if usart < 2:
                    try:
                        self.set_uart7()
                        self.set_uart8()
                        self.set_usart1()
                        self.set_usart2()
                    except Exception as exc2:
                        if str(exc2) == "Не удаётся разместить UART 7":
                            self.u_map_8123(usart)

                        if str(exc2) == "Не удаётся разместить UART 8":
                            self.u_map_123(usart)

                        if str(exc2) == "Не удаётся разместить USART 1":
                            self.u_map_23()

                        if str(exc2) == "Не удаётся разместить USART 2":
                            self.u_map_3()
                else:
                    raise Exception("Не удаётся разместить UART")

            if str(exc) == "Не удаётся разместить UART 7":
                if usart < 2:
                    try:
                        self.set_uart8()
                        self.set_usart1()
                        self.set_usart2()
                    except Exception as exc2:
                        if str(exc2) == "Не удаётся разместить UART 8":
                            self.u_map_123(usart)

                        if str(exc2) == "Не удаётся разместить USART 1":
                            self.u_map_23()

                        if str(exc2) == "Не удаётся разместить USART 2":
                            self.u_map_3()
                else:
                    raise Exception("Не удаётся разместить UART")

            if str(exc) == "Не удаётся разместить UART 8":
                if usart < 2:
                    try:
                        self.set_usart1()
                        self.set_usart2()
                    except Exception as exc2:
                        if str(exc2) == "Не удаётся разместить USART 1":
                            self.u_map_23()

                        if str(exc2) == "Не удаётся разместить USART 2":
                            self.u_map_3()
                else:
                    raise Exception("Не удаётся разместить UART")

            if str(exc) == "Не удаётся разместить USART 1":
                try:
                    self.set_usart2()
                except:
                    self.u_map_3()


    def set_7_uarts(self, usart):
        try:
            self.set_uart4()
            self.set_uart5()
            self.set_uart6()
            self.set_uart7()
            self.set_uart8()
            self.set_usart1()
            self.set_usart2()
        except Exception as exc:
            if str(exc) == "Не удаётся разместить UART 4":
                if usart < 1:
                    try:
                        self.set_uart5()
                        self.set_uart6()
                        self.set_uart7()
                        self.set_uart8()
                        self.set_usart1()
                        self.set_usart2()
                        self.set_usart3()
                    except:
                        raise Exception("Не удаётся разместить UART")
                else:
                    raise Exception("Не удаётся разместить UART")

            if str(exc) == "Не удаётся разместить UART 5":
                self.u_map_678123(usart)

            if str(exc) == "Не удаётся разместить UART 6":
                self.u_map_78123(usart)

            if str(exc) == "Не удаётся разместить UART 7":
                self.u_map_8123(usart)

            if str(exc) == "Не удаётся разместить UART 8":
                self.u_map_123(usart)

            if str(exc) == "Не удаётся разместить USART 1":
                self.u_map_23()

            if str(exc) == "Не удаётся разместить USART 2":
                self.u_map_3()


    def set_8_uarts(self):
        try:
            self.set_uart4()
            self.set_uart5()
            self.set_uart6()
            self.set_uart7()
            self.set_uart8()
            self.set_usart1()
            self.set_usart2()
            self.set_usart3()
        except:
            raise Exception("Не удаётся разместить UART")


    def u_map_3(self, usart):
        if usart < 1:
            self.u_map_3()
        else:
            raise Exception("Не удаётся разместить UART")


    def u_map_3(self):
        try:
            self.set_usart3()
        except:
            raise Exception("Не удаётся разместить UART")


    def u_map_2_3(self, usart):
        if usart < 2:
            try:
                self.set_usart2()
            except:
                self.u_map_3(usart)
        else:
            raise Exception("Не удаётся разместить UART")


    def u_map_1_2_3(self, usart):
        if usart < 3:
            try:
                self.set_usart1()
            except:
                self.u_map_2_3(usart)
        else:
            raise Exception("Не удаётся разместить UART")


    def u_map_8_1_2_3(self, usart):
        try:
            self.set_uart8()
        except:
            self.u_map_1_2_3(usart)


    def u_map_7_8_1_2_3(self, usart):
        try:
            self.set_uart7()
        except:
            self.u_map_8_1_2_3(usart)


    def u_map_6_7_8_1_2_3(self, usart):
        try:
            self.set_uart6()
        except:
            self.u_map_7_8_1_2_3(usart)


    def u_map_23(self, usart):
        if usart < 1:
            self.u_map_23()
        else:
            raise Exception("Не удаётся разместить UART")


    def u_map_23(self):
        try:
            self.set_usart2()
            self.set_usart3()
        except:
            raise Exception("Не удаётся разместить UART")


    def u_map_123(self, usart):
        if usart < 1:
            try:
                self.set_usart1()
                self.set_usart2()
                self.set_usart3()
            except:
                raise Exception("Не удаётся разместить UART")
        else:
            raise Exception("Не удаётся разместить UART")


    def u_map_8123(self, usart):
        if usart < 1:
            try:
                self.set_uart8()
                self.set_usart1()
                self.set_usart2()
                self.set_usart3()
            except:
                raise Exception("Не удаётся разместить UART")
        else:
            raise Exception("Не удаётся разместить UART")


    def u_map_78123(self, usart):
        if usart < 1:
            try:
                self.set_uart7()
                self.set_uart8()
                self.set_usart1()
                self.set_usart2()
                self.set_usart3()
            except:
                raise Exception("Не удаётся разместить UART")
        else:
            raise Exception("Не удаётся разместить UART")


    def u_map_678123(self, usart):
        if usart < 1:
            try:
                self.set_uart6()
                self.set_uart7()
                self.set_uart8()
                self.set_usart1()
                self.set_usart2()
                self.set_usart3()
            except:
                raise Exception("Не удаётся разместить UART")
        else:
            raise Exception("Не удаётся разместить UART")


    def u_map_12_23_3(self, usart):
        if usart < 2:
            try:
                self.set_usart1()
                self.set_usart2()
            except Exception as u_map_12_23_3_exc:
                if str(u_map_12_23_3_exc) == "Не удаётся разместить USART 1":
                    self.u_map_23(usart)

                if str(u_map_12_23_3_exc) == "Не удаётся разместить USART 2":
                    self.u_map_3(usart)
        else:
            raise Exception("Не удаётся разместить UART")


    def u_map_81_12_23_3_2_3(self, usart):
        if usart < 3:
            try:
                self.set_uart8()
                self.set_usart1()
            except Exception as u_map_81_12_23_3_2_3_exc:
                if str(u_map_81_12_23_3_2_3_exc) == "Не удаётся разместить UART 8":
                    self.u_map_12_23_3(usart)

                if str(u_map_81_12_23_3_2_3_exc) == "Не удаётся разместить USART 1":
                    self.u_map_2_3(usart)
        else:
            raise Exception("Не удаётся разместить UART")


    def u_map_812_123_23_3(self, usart):
        if usart < 2:
            try:
                self.set_uart8()
                self.set_usart1()
                self.set_usart2()
            except Exception as u_map_812_123_23_3_exc:
                if str(u_map_812_123_23_3_exc) == "Не удаётся разместить UART 8":
                    self.u_map_123(usart)

                if str(u_map_812_123_23_3_exc) == "Не удаётся разместить USART 1":
                    self.u_map_23(usart)

                if str(u_map_812_123_23_3_exc) == "Не удаётся разместить USART 2":
                    self.u_map_3(usart)
        else:
            raise Exception("Не удаётся разместить UART")


    def u_map_7812_8123_123_23_3(self, usart):
        if usart < 2:
            try:
                self.set_uart7()
                self.set_uart8()
                self.set_usart1()
                self.set_usart2()
            except Exception as u_map_7812_8123_123_23_3_exc:
                if str(u_map_7812_8123_123_23_3_exc) == "Не удаётся разместить UART 7":
                    self.u_map_8123(usart)

                if str(u_map_7812_8123_123_23_3_exc) == "Не удаётся разместить UART 8":
                    self.u_map_123(usart)

                if str(u_map_7812_8123_123_23_3_exc) == "Не удаётся разместить USART 1":
                    self.u_map_23(usart)

                if str(u_map_7812_8123_123_23_3_exc) == "Не удаётся разместить USART 2":
                    self.u_map_3(usart)
        else:
            raise Exception("Не удаётся разместить UART")


    def u_map_781_812_123_23_3(self, usart):
        if usart < 3:
            try:
                self.set_uart7()
                self.set_uart8()
                self.set_usart1()
            except Exception as u_map_781_812_123_23_3_exc:
                if str(u_map_781_812_123_23_3_exc) == "Не удаётся разместить UART 7":
                    self.u_map_812_123_23_3(usart)

                if str(u_map_781_812_123_23_3_exc) == "Не удаётся разместить UART 8":
                    self.u_map_12_23_3(usart)

                if str(u_map_781_812_123_23_3_exc) == "Не удаётся разместить USART 1":
                    self.u_map_2_3(usart)
        else:
            raise Exception("Не удаётся разместить UART")


    def u_map_6781_7812_8123_123_23_3(self, usart):
        if usart < 3:
            try:
                self.set_uart6()
                self.set_uart7()
                self.set_uart8()
                self.set_usart1()
            except Exception as u_map_6781_7812_8123_123_23_3_exc:
                if str(u_map_6781_7812_8123_123_23_3_exc) == "Не удаётся разместить UART 6":
                    self.u_map_7812_8123_123_23_3(usart)

                if str(u_map_6781_7812_8123_123_23_3_exc) == "Не удаётся разместить UART 7":
                    self.u_map_812_123_23_3(usart)

                if str(u_map_6781_7812_8123_123_23_3_exc) == "Не удаётся разместить UART 8":
                    self.u_map_12_23_3(usart)

                if str(u_map_6781_7812_8123_123_23_3_exc) == "Не удаётся разместить USART 1":
                    self.u_map_2_3(usart)
        else:
            raise Exception("Не удаётся разместить UART")


    def u_map_78_81_12_23_3_2_3(self, usart):
        try:
            self.set_uart7()
            self.set_uart8()
        except Exception as u_map_78_81_12_23_3_2_3_exc:
            if str(u_map_78_81_12_23_3_2_3_exc) == "Не удаётся разместить UART 7":
                self.u_map_81_12_23_3_2_3(usart)

            if str(u_map_78_81_12_23_3_2_3_exc) == "Не удаётся разместить UART 8":
                self.u_map_1_2_3(usart)


    def u_map_678_781_812_123_23_3(self, usart):
        try:
            self.set_uart6()
            self.set_uart7()
            self.set_uart8()
        except Exception as u_map_678_781_812_123_23_3_exc:
            if str(u_map_678_781_812_123_23_3_exc) == "Не удаётся разместить UART 6":
                self.u_map_781_812_123_23_3(usart)

            if str(u_map_678_781_812_123_23_3_exc) == "Не удаётся разместить UART 7":
                self.u_map_81_12_23_3_2_3(usart)

            if str(u_map_678_781_812_123_23_3_exc) == "Не удаётся разместить UART 8":
                self.u_map_1_2_3(usart)


    def u_map_67_78_81_12_23_3_2_3(self, usart):
        try:
            self.set_uart6()
            self.set_uart7()
        except Exception as u_map_67_78_81_12_23_3_2_3_exc:
            if str(u_map_67_78_81_12_23_3_2_3_exc) == "Не удаётся разместить UART 6":
                self.u_map_78_81_12_23_3_2_3(usart)

            if str(u_map_67_78_81_12_23_3_2_3_exc) == "Не удаётся разместить UART 7":
                self.u_map_8_1_2_3(usart)


    def set_uart4(self):
        if self.pins['C'][10] == "GPIO" and self.pins['C'][11] == "GPIO":
            self.pins['C'][10] = "UART4_TX"
            self.pins['C'][11] = "UART4_RX"
        else:
            if not(self.remap1_uart4()):
                if not(self.remap2_uart4()):
                    raise Exception(f"Не удаётся разместить UART 4")


    def remap1_uart4(self):
        if self.pins['B'][0] == "ETH_MII_RXD2":
            if not(self.remap_eth_mii()):
                return False

        if self.pins['B'][0] == "GPIO" and self.pins['B'][1] == "GPIO":
            self.pins['B'][0] = "UART4_TX"
            self.pins['B'][1] = "UART4_RX"
            return True
        else:
            return False


    def remap2_uart4(self):
        if self.pins['E'][0] == "GPIO" and self.pins['E'][1] == "GPIO":
            self.pins['E'][0] = "UART4_TX"
            self.pins['E'][1] = "UART4_RX"
            return True
        else:
            return False


    def set_uart5(self):
        if self.pins['C'][12] == "GPIO" and self.pins['D'][2] == "GPIO":
            self.pins['C'][12] = "UART5_TX"
            self.pins['D'][2]  = "UART5_RX"
        else:
            if not(self.remap1_uart5()):
                if not(self.remap2_uart5()):
                    raise Exception(f"Не удаётся разместить UART 5")


    def remap1_uart5(self):
        if self.pins['B'][4] == "GPIO" and self.pins['B'][5] == "GPIO":
            self.pins['B'][4] = "UART5_TX"
            self.pins['B'][5] = "UART5_RX"
            return True
        else:
            return False


    def remap2_uart5(self):
        if self.pins['E'][8] == "GPIO" and self.pins['E'][9] == "GPIO":
            self.pins['E'][8] = "UART5_TX"
            self.pins['E'][9] = "UART5_RX"
            return True
        else:
            return False


    def set_uart6(self):
        if self.pins['C'][0] == "GPIO" and self.pins['C'][1] == "GPIO":
            self.pins['C'][0] = "UART6_TX"
            self.pins['C'][1] = "UART6_RX"
        else:
            if not(self.remap1_uart6()):
                if not(self.remap2_uart6()):
                    raise Exception(f"Не удаётся разместить UART 6")


    def remap1_uart6(self):
        if self.pins['B'][8] == "GPIO" and self.pins['B'][9] == "GPIO":
            self.pins['B'][8] = "UART6_TX"
            self.pins['B'][9] = "UART6_RX"
            return True
        else:
            return False


    def remap2_uart6(self):
        if self.pins['E'][10] == "GPIO" and self.pins['E'][11] == "GPIO":
            self.pins['E'][10] = "UART6_TX"
            self.pins['E'][11] = "UART6_RX"
            return True
        else:
            return False


    def set_uart7(self):
        if self.pins['C'][2] == "GPIO" and self.pins['C'][3] == "GPIO":
            self.pins['C'][2] = "UART7_TX"
            self.pins['C'][3] = "UART7_RX"
        else:
            if not(self.remap1_uart7()):
                if not(self.remap2_uart7()):
                    raise Exception(f"Не удаётся разместить UART 7")


    def remap1_uart7(self):
        if self.pins['A'][7] == "ETH_RMII_CRS_DV":
            if not(self.remap_eth_rmii()):
                return False

        if self.pins['A'][7] == "ETH_MII_RX_DV":
            if not(self.remap_eth_mii()):
                return False

        if self.pins['A'][6] == "GPIO" and self.pins['A'][7] == "GPIO":
            self.pins['A'][6] = "UART7_TX"
            self.pins['A'][7] = "UART7_RX"
            return True
        else:
            return False


    def remap2_uart7(self):
        if self.pins['E'][12] == "GPIO" and self.pins['E'][13] == "GPIO":
            self.pins['E'][12] = "UART7_TX"
            self.pins['E'][13] = "UART7_RX"
            return True
        else:
            return False


    def set_uart8(self):
        if self.pins['C'][4] == "ETH_RMII_RXD0":
            if not(self.remap_eth_rmii()):
                return False

        if self.pins['C'][4] == "ETH_MII_RXD0":
            if not(self.remap_eth_mii()):
                return False

        if self.pins['C'][4] == "GPIO" and self.pins['C'][5] == "GPIO":
            self.pins['C'][4] = "UART8_TX"
            self.pins['C'][5] = "UART8_RX"
        else:
            if not(self.remap1_uart8()):
                if not(self.remap2_uart8()):
                    raise Exception(f"Не удаётся разместить UART 8")


    def remap1_uart8(self):
        if self.pins['A'][14] == "GPIO" and self.pins['A'][15] == "GPIO":
            self.pins['A'][14] = "UART8_TX"
            self.pins['A'][15] = "UART8_RX"
            return True
        else:
            return False


    def remap2_uart8(self):
        if self.pins['E'][14] == "GPIO" and self.pins['E'][15] == "GPIO":
            self.pins['E'][14] = "UART8_TX"
            self.pins['E'][15] = "UART8_RX"
            return True
        else:
            return False


    def set_adc(self, value):
        i = 0
        self.flag_check_mii = True
        self.flag_check_rmii = True
        while i < value:
            self.set_adc_ch()
            i += 1


    def set_adc_ch(self):
        if self.pins['A'][0] == "GPIO":
            self.pins['A'][0] = "ADC_IN0"
        elif self.pins['A'][1] == "GPIO":
            self.pins['A'][1] = "ADC_IN1"
        elif self.pins['A'][2] == "GPIO":
            self.pins['A'][2] = "ADC_IN2"
        elif self.pins['A'][3] == "GPIO":
            self.pins['A'][3] = "ADC_IN3"
        elif self.pins['A'][4] == "GPIO":
            self.pins['A'][4] = "ADC_IN4"
        elif self.pins['A'][5] == "GPIO":
            self.pins['A'][5] = "ADC_IN5"
        elif self.pins['A'][6] == "GPIO":
            self.pins['A'][6] = "ADC_IN6"
        elif self.pins['A'][7] == "GPIO":
            self.pins['A'][7] = "ADC_IN7"
        elif self.pins['A'][7] == "ETH_RMII_CRS_DV" and self.flag_check_rmii:
            if self.remap_eth_rmii():
                self.pins['A'][7] = "ADC_IN7"
            else:
                self.flag_check_rmii = False
        elif self.pins['A'][7] == "ETH_MII_RX_DV" and self.flag_check_mii:
            if self.remap_eth_mii():
                self.pins['A'][7] = "ADC_IN7"
            else:
                self.flag_check_mii = False
        elif self.pins['B'][0] == "GPIO":
            self.pins['B'][0] = "ADC_IN8"
        elif self.pins['B'][1] == "GPIO":
            self.pins['B'][1] = "ADC_IN9"
        elif self.pins['C'][0] == "GPIO":
            self.pins['C'][0] = "ADC_IN10"
        elif self.pins['C'][1] == "GPIO":
            self.pins['C'][1] = "ADC_IN11"
        elif self.pins['C'][2] == "GPIO":
            self.pins['C'][2] = "ADC_IN12"
        elif self.pins['C'][3] == "GPIO":
            self.pins['C'][3] = "ADC_IN13"
        elif self.pins['C'][4] == "GPIO":
            self.pins['C'][4] = "ADC_IN14"
        elif self.pins['C'][5] == "GPIO":
            self.pins['C'][5] = "ADC_IN15"
        else:
            raise Exception(f"Не удаётся разместить ADC")


    def set_exti(self, value):
        i = 0
        for j in range(0, 16):
            if i == value:
                break
            if self.pins['A'][j] == "GPIO":
                self.pins['A'][j] = f"EXTI{i}"
                i += 1
            elif self.pins['B'][j] == "GPIO":
                self.pins['B'][j] = f"EXTI{i}"
                i += 1
            elif self.pins['C'][j] == "GPIO":
                self.pins['C'][j] = f"EXTI{i}"
                i += 1
            elif self.pins['D'][j] == "GPIO":
                self.pins['D'][j] = f"EXTI{i}"
                i += 1
            elif self.pins['E'][j] == "GPIO":
                self.pins['E'][j] = f"EXTI{i}"
                i += 1
        if value > i:
            raise Exception(f"Не удаётся разместить требуемое количество EXTI")


    def set_gpio(self, value):
        i = 0
        for j in range(0, 16):
            if self.pins['A'][j] == "GPIO":
                i += 1
            if self.pins['B'][j] == "GPIO":
                i += 1
            if self.pins['C'][j] == "GPIO":
                i += 1
            if self.pins['D'][j] == "GPIO":
                i += 1
            if self.pins['E'][j] == "GPIO":
                i += 1
        if value > i:
            raise Exception("Не остаётся требуемое количество GPIO\n" + 
                            f"Всего доступны после размещения {i} GPIO")


    def add_pins_to_layout(self):
        for i in range(0, 16):
            self.wid_layout.addWidget(QLabel(f"A{i} = {self.pins['A'][i]}"), i, 0)
            self.wid_layout.addWidget(QLabel(f"B{i} = {self.pins['B'][i]}"), i, 1)
            self.wid_layout.addWidget(QLabel(f"C{i} = {self.pins['C'][i]}"), i, 2)
            self.wid_layout.addWidget(QLabel(f"D{i} = {self.pins['D'][i]}"), i, 3)
            self.wid_layout.addWidget(QLabel(f"E{i} = {self.pins['E'][i]}"), i, 4)


    def on_bn2_pressed(self):
        self.stackedWidget.setCurrentIndex(0)
        self.setMinimumSize(660, 500)
        if not(self.windowState() & Qt.WindowState.WindowMaximized):
            self.resize(560, 480)


    def on_bnSave_pressed(self):
        CustomDialog(self.pins, True)


    def on_bn3_pressed(self):
        for i in reversed(range(self.secondPageLayout.count())):
            self.secondPageLayout.itemAt(i).widget().setParent(None)
        
        self.setMinimumSize(1200, 640)
        wid = QWidget()
        self.wid_layout = QGridLayout()
        self.set_lqfp100()
        self.add_lqfp100_to_layout()
        wid.setLayout(self.wid_layout)

        bn2 = QPushButton("Назад")
        bn2.clicked.connect(self.on_bn2_pressed)

        bn4 = QPushButton("Результат размещения (Pins)")
        bn4.clicked.connect(self.on_bn_pressed)

        bnSave2 = QPushButton("Cохранить результат размещения")
        bnSave2.clicked.connect(self.on_bnSave2_pressed)

        self.secondPageLayout.addWidget(wid, 0, 0, 1, 3)
        self.secondPageLayout.addWidget(bn2, 1, 0)
        self.secondPageLayout.addWidget(bn4, 1, 1)
        self.secondPageLayout.addWidget(bnSave2, 1, 2)
        self.secondPageWidget.update()
    

    def on_bnSave2_pressed(self):
        CustomDialog(self.lqfp100, False)


    def set_lqfp100(self):
        for i in range(1, 6):
            self.lqfp100[i] = f"PE{i+1} = {self.pins['E'][i+1]}"
        self.lqfp100[6] = "VBAT"
        for i in range(7, 10):
            self.lqfp100[i] = f"PC{i+6} = {self.pins['C'][i+6]}"
        self.lqfp100[10] = "VSS_5"
        self.lqfp100[11] = "VDD_5"
        self.lqfp100[12] = "OSC_IN"
        self.lqfp100[13] = "OSC_OUT"
        self.lqfp100[14] = "NRST"
        for i in range(15, 19):
            self.lqfp100[i] = f"PC{i-15} = {self.pins['C'][i-15]}"
        self.lqfp100[19] = "VSSA"
        self.lqfp100[20] = "VREF-"
        self.lqfp100[21] = "VREF+"
        self.lqfp100[22] = "VDDA"
        for i in range(23, 27):
            self.lqfp100[i] = f"PA{i-23} = {self.pins['A'][i-23]}"
        self.lqfp100[27] = "VSS_4"
        self.lqfp100[28] = "VDD_4"
        for i in range(29, 33):
            self.lqfp100[i] = f"PA{i-25} = {self.pins['A'][i-25]}"
        for i in range(33, 35):
            self.lqfp100[i] = f"PC{i-29} = {self.pins['C'][i-29]}"
        for i in range(35, 38):
            self.lqfp100[i] = f"PB{i-35} = {self.pins['B'][i-35]}"
        for i in range(38, 47):
            self.lqfp100[i] = f"PE{i-31} = {self.pins['E'][i-31]}"
        for i in range(47, 49):
            self.lqfp100[i] = f"PB{i-37} = {self.pins['B'][i-37]}"
        self.lqfp100[49] = "VSS_1"
        self.lqfp100[50] = "VIO_1"
        for i in range(51, 55):
            self.lqfp100[i] = f"PB{i-39} = {self.pins['B'][i-39]}"
        for i in range(55, 63):
            self.lqfp100[i] = f"PD{i-47} = {self.pins['D'][i-47]}"
        for i in range(63, 67):
            self.lqfp100[i] = f"PC{i-57} = {self.pins['C'][i-57]}"
        for i in range(67, 73):
            self.lqfp100[i] = f"PA{i-59} = {self.pins['A'][i-59]}"
        self.lqfp100[73] = "NC"
        self.lqfp100[74] = "VSS_2"
        self.lqfp100[75] = "VDD_2"
        for i in range(76, 78):
            self.lqfp100[i] = f"PA{i-62} = {self.pins['A'][i-62]}"
        for i in range(78, 81):
            self.lqfp100[i] = f"PC{i-68} = {self.pins['C'][i-68]}"
        for i in range(81, 89):
            self.lqfp100[i] = f"PD{i-81} = {self.pins['D'][i-81]}"
        for i in range(89, 94):
            self.lqfp100[i] = f"PB{i-86} = {self.pins['B'][i-86]}"
        self.lqfp100[94] = "BOOT0"
        for i in range(95, 97):
            self.lqfp100[i] = f"PB{i-87} = {self.pins['B'][i-87]}"
        for i in range(97, 99):
            self.lqfp100[i] = f"PE{i-97} = {self.pins['E'][i-97]}"
        self.lqfp100[99] = "VSS_3"
        self.lqfp100[100] = "VIO_3"
        

    def add_lqfp100_to_layout(self):
        for i in range(1, 21):
            self.wid_layout.addWidget(QLabel(f"{i} = {self.lqfp100[i]}"), i, 0)
            self.wid_layout.addWidget(QLabel(f"{20 + i} = {self.lqfp100[20 + i]}"), i, 1)
            self.wid_layout.addWidget(QLabel(f"{40 + i} = {self.lqfp100[40 + i]}"), i, 2)
            self.wid_layout.addWidget(QLabel(f"{60 + i} = {self.lqfp100[60 + i]}"), i, 3)
            self.wid_layout.addWidget(QLabel(f"{80 + i} = {self.lqfp100[80 + i]}"), i, 4)


class CustomDialog(QDialog):
    def __init__(self, result_dict, pins_or_lqfp100):
        super().__init__()
        self.result_dict = result_dict
        if pins_or_lqfp100:
            self.file_name = 'pins.json'
        else:
            self.file_name = 'lqfp100.json'

        self.setWindowTitle("CH32V307 Pins")
        self.layout = QVBoxLayout()
        is_json_file_not_exist = not(os.path.exists(f"{os.getcwd()}/{self.file_name}"))
        if is_json_file_not_exist:
            self.acceptSave()
            buttonOk = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
            buttonOk.accepted.connect(self.accept)
            message = QLabel(f"Результат размещения был записан в файл {self.file_name}")
            self.layout.addWidget(message)
            self.layout.addWidget(buttonOk)
        else:
            buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            buttonBox.accepted.connect(self.acceptSave)
            buttonBox.rejected.connect(self.reject)
            message = QLabel(f"При сохранении результата будет перезаписан файл {self.file_name}\nСохранить результат размещения?")
            self.layout.addWidget(message)
            self.layout.addWidget(buttonBox)
        self.setLayout(self.layout)
        self.exec()


    def acceptSave(self):
        with open(self.file_name, 'w', encoding='utf-8') as f:
            json.dump(self.result_dict, f, indent=4)
        self.close()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
