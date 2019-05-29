<?php

        $output = passthru('cd /home/ubuntu/yoloface/ && ls && python3 delete_known.py');
        echo $output;
?>
