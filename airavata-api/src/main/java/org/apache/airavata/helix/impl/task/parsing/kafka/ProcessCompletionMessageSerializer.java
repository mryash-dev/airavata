/**
*
* Licensed to the Apache Software Foundation (ASF) under one
* or more contributor license agreements. See the NOTICE file
* distributed with this work for additional information
* regarding copyright ownership. The ASF licenses this file
* to you under the Apache License, Version 2.0 (the
* "License"); you may not use this file except in compliance
* with the License. You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing,
* software distributed under the License is distributed on an
* "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
* KIND, either express or implied. See the License for the
* specific language governing permissions and limitations
* under the License.
*/
package org.apache.airavata.helix.impl.task.parsing.kafka;

import java.util.Map;
import org.apache.airavata.helix.impl.task.parsing.ProcessCompletionMessage;
import org.apache.kafka.common.serialization.Serializer;

public class ProcessCompletionMessageSerializer implements Serializer<ProcessCompletionMessage> {

    @Override
    public void configure(Map<String, ?> configs, boolean isKey) {}

    @Override
    public byte[] serialize(String topic, ProcessCompletionMessage data) {
        String serialized = data.getProcessId() + ";" + data.getExperimentId() + ";" + data.getGatewayId();
        return serialized.getBytes();
    }

    @Override
    public void close() {}
}
