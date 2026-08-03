今天发现以前合并单元格并没有生效，经过研究发现已下结论：

- 表格的样式宽度支持四种 NIL、TWIP、AUTO、PERCENT 分别代表无宽度、TWIP word基本单位、自动、百分比
- 百分比是 1% 代表50份 TWIP
- 合并单元格，并不会自动实现自动宽度，比如两行三列单元格， 合并第一行前两列，最终得到的是第一行两个cell，第一个cell和原第一个cell宽度相等
- 如果想要合并单元格 且保证最终合并单元格 的宽度和我们想要的宽度一致，唯一的办法是设置表格宽度后，给每行里的每个单元格设置宽度, 如果设置百分比， 总table 占文档100% 设为5000，然后按照每个单元格自己想要的百分比去设置N*50
- 合并单元格是通过设置cell的样式实现`['gridSpan' => 2, 'valign' => 'center']`

``` 官方示例
/*
 *  3. colspan (gridSpan) and rowspan (vMerge)
 *  ---------------------
 *  |     |   B    |    |
 *  |  A  |--------|  E |
 *  |     | C |  D |    |
 *  ---------------------
 */

$section->addPageBreak();
$section->addText('Table with colspan and rowspan', $header);

$fancyTableStyle = array('borderSize' => 6, 'borderColor' => '999999');
$cellRowSpan = array('vMerge' => 'restart', 'valign' => 'center', 'bgColor' => 'FFFF00');
$cellRowContinue = array('vMerge' => 'continue');
$cellColSpan = array('gridSpan' => 2, 'valign' => 'center');
$cellHCentered = array('alignment' => \PhpOffice\PhpWord\SimpleType\Jc::CENTER);
$cellVCentered = array('valign' => 'center');

$spanTableStyleName = 'Colspan Rowspan';
$phpWord->addTableStyle($spanTableStyleName, $fancyTableStyle);
$table = $section->addTable($spanTableStyleName);

$table->addRow();

$cell1 = $table->addCell(2000, $cellRowSpan);
$textrun1 = $cell1->addTextRun($cellHCentered);
$textrun1->addText('A');
$textrun1->addFootnote()->addText('Row span');

$cell2 = $table->addCell(4000, $cellColSpan);
$textrun2 = $cell2->addTextRun($cellHCentered);
$textrun2->addText('B');
$textrun2->addFootnote()->addText('Column span');

$table->addCell(2000, $cellRowSpan)->addText('E', null, $cellHCentered);

$table->addRow();
$table->addCell(null, $cellRowContinue);
$table->addCell(2000, $cellVCentered)->addText('C', null, $cellHCentered);
$table->addCell(2000, $cellVCentered)->addText('D', null, $cellHCentered);
$table->addCell(null, $cellRowContinue);


```
自己做的
```
$table = new Table(array(
            'borderSize'  => 6,
            'borderColor' => 'black',
            'width'       => 5000,
            'unit'        => TblWidth::PERCENT,
            'align'      => 'center',
        ));

        $header_style = [
            'bold' => true,
            'size' => 9
        ];
        $paragraphStyle = [
            'align'=>'center',
        ];
        $fontStyle = [
            'size'  => 9,
        ];
        $table->addRow();
        $table->addCell(39*50)->addText('名称', $header_style, $paragraphStyle);
        $table->addCell(3*50)->addText('申请号', $header_style, $paragraphStyle);
        $table->addCell(3*50)->addText('类型', $header_style, $paragraphStyle);
        $table->addCell(14*50)->addText('缴费年份', $header_style, $paragraphStyle);
        $table->addCell(26*50)->addText('缴纳年费日期范围', $header_style, $paragraphStyle);
        $table->addCell(3*50)->addText('年费', $header_style, $paragraphStyle);
        $table->addCell(10*50)->addText('滞纳金', $header_style, $paragraphStyle);
        $table->addCell(6*50)->addText('滞纳金绝限日', $header_style, $paragraphStyle);
        $table->addCell(6*50)->addText('维护费', $header_style, $paragraphStyle);
        $total = 0;
        if($cases){
            foreach($cases as $key=>&$value){
                $table->addRow();
                $table->addCell(39*50)->addText($value['name'], $fontStyle);
                $table->addCell(3*50)->addText($value['apply_no'], $fontStyle);
                $table->addCell(3*50)->addText($value['type'], $fontStyle);
                $table->addCell(14*50)->addText($value['to_year'], $fontStyle);
                $table->addCell(26*50)->addText($value['year_fee_area'], $fontStyle);
                $table->addCell(3*50)->addText((int)$value['year_fee'], $fontStyle);
                $table->addCell(10*50)->addText((int)$value['late_fee'], $fontStyle);
                $table->addCell(6*50)->addText($value['late_fee_end'], $fontStyle);
                $table->addCell(6*50)->addText($value['service_price'], $fontStyle);
                $total+= (int)($value['year_fee'] + (int)$value['late_fee'] + (int)$value['service_price']);
            }
        }
        $table->addRow();
        $table->addCell(94*50, ['valign'=>'center', 'gridSpan' => 8, 'unit'=>'pct'])->addText('合计', $header_style, $paragraphStyle);
        $table->addCell(6*50, ['unit'=>'pct'])->addText($total, $header_style, $paragraphStyle);
        $templateProcessor->setComplexBlock('table', $table);
```
从而实现了动态生成word中带合并单元格（汇总统计）的功能

![Dingtalk_20210303202156](https://user-images.githubusercontent.com/1614114/109805637-add32c80-7c5e-11eb-980c-dfc3a4c17065.jpg)


>参考官方sample Sample_09_Tables.php
> 如果模板文档里有多个同名的变量， 需要`$templateProcessor->setComplexValue('company', new Text($config['company']));
        $templateProcessor->setComplexValue('company', new Text($config['company']));`  多次

