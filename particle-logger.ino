
int iCoutn;
String aString;

void setup()
{
    iCoutn = 0;
    Particle.variable("data", aString);
}

void loop()
{
    iCoutn++;
    aString = String::format("%d,%d,%d,%d,%d", iCoutn, iCoutn, iCoutn, iCoutn, iCoutn);
    delay(1000);
}
