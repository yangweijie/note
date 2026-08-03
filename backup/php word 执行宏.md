```
try {
        $word = new \COM("word.application") or die("Can't start Word!");
        $word->Visible = 0;
        $word->Documents->Open($srcfilename, false, false, false, "1", "1", true);
        $word->ActiveDocument->final = false;
        $word->ActiveDocument->Saved = true;
        $word->Application->run('getPageCount');
        // $word->Documents[1]->SaveAs($destfilename);
		$word->ActiveDocument->ExportAsFixedFormat(
			$destfilename,
			17, // wdExportFormatPDF
			false, // open file after export
			0, // wdExportOptimizeForPrint
			3, // wdExportFromTo
			1, // begin page
			5000, // end page
			7, // wdExportDocumentWithMarkup
			true, // IncludeDocProps
			true, // KeepIRM
			1// WdExportCreateBookmarks
		);
		$word->ActiveDocument->Close();
        $end = time();
        $word->Quit();
    } catch (\Exception $e) {
        if (method_exists($word, "Quit")) {
            $word->Quit();
        }
        $error = $e->getCode().PHP_EOL.$e->getMessage().PHP_EOL.$e->getTraceAsString();
        // ptrace($e->getCode());
        // ptrace($error);
        $end = time();
    }
```
名称为word中定义的宏，测试可以把 Visible  = 1 和加 sleep 来看是否执行成功