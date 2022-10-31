2019.01.02
main.py
def main():
    #maxrange, mV, lamda
    BeamModel.BeamModel(120, 5.0, 0.5)
    WeighingFactors.WeighingFactors(1.0, 0.1, 0.0, 0.1)
Ponits.py
def MonteCarloLocalization(particleCount):
    DeltaR = 3.0

VelocityModel.py
A = [0.001, 0.001, 0.001, 0.001, 0.001, 0.001]

修改设置粒子总数的方法，现在只需要在Main.py中修改一次
--------------------------------------------------------
2018.12.17

A = [10, 10, 5, 5, 10, 10]
效果：可收敛，不同步，最后粒子呈发散状

A = [10, 10, 10, 10, 10, 10]
效果：收敛，定位不准

重写velocityModel.Sample()
存在问题：机器人转向后定位不准

测试Points.py中的DeltaR影响粒子预测的范围