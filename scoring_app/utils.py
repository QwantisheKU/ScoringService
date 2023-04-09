from .models import Calculation
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

def create_word_results(print_query):
    document = Document()
    styles = document.styles

    paragraph_styles = document.styles['Normal']
    paragraph_font = paragraph_styles.font
    paragraph_font.name = 'Times New Roman'
    paragraph_font.size = Pt(14)

    new_heading_style = styles.add_style('New Heading', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Heading 1']

    heading_font = new_heading_style.font
    heading_font.name = 'Times New Roman'
    heading_font.size = Pt(16)
    heading_font.color.rgb = RGBColor(0, 0, 0)

    heading = document.add_paragraph(f'Ваш кредитный риск профиль\n', style='New Heading')
    heading.add_run(f'{print_query["score"]}')
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    #heading.paragraph_format.space_after = Pt(20)

    if print_query['recommendations']:
        paragraph = document.add_paragraph('')
        paragraph = document.add_paragraph('Рекомендации:')

    for recommendation in print_query['recommendations'].values():
        paragraph = document.add_paragraph(recommendation, style='List Number')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    document.save('static/files/Результат расчета.docx')


def check_recommendations(request, calculation_id):
    
    recommendations = {}
    calculation = Calculation.objects.get(id = calculation_id)
    
    # P = D x F x K, где P - платежеспособность заемщика, D – ежемесячный доход после уплаты налогов, F – срок кредита или займа в месяцах, а К – поправочный коэффициент (если D меньше $500, то К равен 0,3; если D более $500, но менее $1000, то К равен 0,4; если D больше $1000, но менее $2000, то К равен 0,5; если D больше $2000, то К равен 0,6)
    k = 0
    if calculation.person_income < 500:
        k = 0.3
    elif calculation.person_income >= 500 and calculation.person_income < 1000:
        k = 0.4
    elif calculation.person_income >= 1000 and calculation.person_income < 2000:
        k = 0.5
    elif calculation.person_income >= 2000:
        k = 0.6
    p = round(calculation.person_income, 2) * calculation.loan_term * k

    # S = P/(1 + (C x (t + 1))/(2*12*100))
    s =  p/(1+(calculation.loan_int_rate*(calculation.loan_term+1))/(2*12*100))

    if calculation.loan_amnt > s:
        recommendations['loan_amount'] = f'Указанная сумма кредита или займа превышает оптимальную. Оптимальная сумма кредита или займа для вашего расчета = {round(s, 2)}$.'

    if calculation.person_home_ownership == 'MORTGAGE':
        recommendations['mortgage'] = 'Зачастую финансовые организации отказывают в предоставлении кредита по причине имеющейся кредитной нагрузки в виде ипотеки. Рекомендуется закрывать все предыдущие кредиты или займы перед взятием новых.'

    if calculation.cb_person_default_on_file == 'Y':
        recommendations['default'] = 'Наличие просроченных, даже на небольшой срок, долгов является "красным флагом" для финансовых организаций, особенно, банковских организаций. Рекомендуется не запаздывать и не откладывать запланированные выплаты, не имея на это жизненно-важных обоснований, даже если ранее имел место быть просроченный кредит или заём.'
    
    if calculation.loan_int_rate > 11:
        recommendations['loan_int_rate'] = 'Указанная процентная ставка превышает среднее значение. Рекомендуется ознакомиться с продуктами других финансовых организаций самостоятельно или обратиться за помощью к сайтам-агрегаторам.'
    
    if calculation.cb_person_default_on_file == 'DEBTCONSOLIDATION':
        recommendations['loan_default'] = 'Финансовые организации в большинстве случаев не оформляют кредиты и займы для погашения предыдущих задолженностей. Рекомендуется закрывать все предыдущие кредиты или займы перед взятием новых.'

    return recommendations

def paginate_calculations(request, calculations, results):

    page = request.GET.get('page')
    paginator = Paginator(calculations, results)
    try:
        calculations = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        calculations = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        calculations = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, calculations
